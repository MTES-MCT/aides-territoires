import json
import requests
import datetime
from collections import defaultdict
from datetime import timedelta
from time import strftime, gmtime
from pathlib import Path

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from django.db.models import Count, Sum
from django.views.generic.edit import FormMixin

from aids.models import Aid, AidProject
from accounts.models import User
from backers.models import Backer
from geofr.models import Perimeter
from geofr.utils import get_all_related_perimeters
from stats.models import AidViewEvent, Event, AidSearchEvent, AidContactClickEvent
from organizations.models import Organization
from projects.models import Project
from search.models import SearchPage
from alerts.models import Alert

from stats.forms import StatSearchForm
from accounts.mixins import SuperUserRequiredMixin
from aids.views import AidPaginator

# The manual percentage threshold to ensure that the metropolitan area
# has enough contrasts between departments. It is not computed because
# some exceptions like Guadeloupe already have 70% of their communes
# with an account!
DEPARTMENTS_ORG_COMMUNES_MAX = "30"

# That table should/could be computed with the `populate_communes`
# command once and for all, annualy from official sources (COG or geoAPI).
# For instance the length of:
# https://geo.api.gouv.fr/communes?fields=nom&codeDepartement=54
# Current source: https://fr.wikipedia.org/wiki/Nombre_de_communes_en_France
NB_COMMUNES_PAR_DEPARTEMENT_2022 = {
    "01": 393,
    "02": 799,
    "03": 317,
    "04": 198,
    "05": 162,
    "06": 163,
    "07": 335,
    "08": 449,
    "09": 327,
    "10": 431,
    "11": 433,
    "12": 285,
    "13": 119,
    "14": 528,
    "15": 246,
    "16": 364,
    "17": 463,
    "18": 287,
    "19": 279,
    "2A": 124,
    "2B": 236,
    "21": 698,
    "22": 348,
    "23": 256,
    "24": 503,
    "25": 571,
    "26": 363,
    "27": 585,
    "28": 365,
    "29": 277,
    "30": 351,
    "31": 586,
    "32": 461,
    "33": 535,
    "34": 342,
    "35": 333,
    "36": 241,
    "37": 272,
    "38": 512,
    "39": 494,
    "40": 327,
    "41": 267,
    "42": 323,
    "43": 257,
    "44": 207,
    "45": 325,
    "46": 313,
    "47": 319,
    "48": 152,
    "49": 177,
    "50": 446,
    "51": 613,
    "52": 426,
    "53": 240,
    "54": 591,
    "55": 499,
    "56": 249,
    "57": 725,
    "58": 309,
    "59": 648,
    "60": 679,
    "61": 385,
    "62": 890,
    "63": 464,
    "64": 546,
    "65": 469,
    "66": 226,
    "67": 514,
    "68": 366,
    "69": 208,
    "69M": 59,
    "70": 539,
    "71": 565,
    "72": 354,
    "73": 273,
    "74": 279,
    "75": 1,
    "76": 708,
    "77": 507,
    "78": 259,
    "79": 256,
    "80": 772,
    "81": 314,
    "82": 195,
    "83": 153,
    "84": 151,
    "85": 257,
    "86": 266,
    "87": 195,
    "88": 507,
    "89": 423,
    "90": 101,
    "91": 194,
    "92": 36,
    "93": 40,
    "94": 47,
    "95": 184,
    "971": 32,
    "972": 34,
    "973": 22,
    "974": 24,
    "976": 17,
}


class StatsView(TemplateView):
    template_name = "stats/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        aids_qs = Aid.objects.live()
        context["nb_live_aids"] = aids_qs.count()

        one_week_ago = timezone.now() - timedelta(days=7)
        viewed_aids_qs = AidViewEvent.objects.filter(date_created__gte=one_week_ago)
        context["nb_viewed_aids"] = viewed_aids_qs.count()

        alerts_qs = Event.objects.filter(category="alert", event="sent").aggregate(
            nb_sent_alerts=Sum("value")
        )
        context["nb_sent_alerts"] = alerts_qs["nb_sent_alerts"]

        active_backers = Backer.objects.has_financed_aids()
        context["nb_backers"] = active_backers.count()

        return context


class DashboardView(SuperUserRequiredMixin, FormMixin, TemplateView):
    template_name = "stats/dashboard.html"
    form_class = StatSearchForm

    def get_period(self):

        period = timezone.now().strftime("%Y-%m-%d")

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                if form.cleaned_data["end_date"]:
                    end_date = form.cleaned_data["end_date"]
                else:
                    end_date = start_date

                start_date = start_date.strftime("%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
                period = start_date.split() + end_date.split()

        return period

    def get_matomo_stats(self, method, period="range", date_="today", **kwargs):
        """
        Here we want to get the stats from Matomo.
        """

        url = "https://stats.data.gouv.fr/"

        params = {
            "idSite": settings.MATOMO_SITE_ID,
            "module": "API",
            "method": method,
            "period": period,
            "date": date_,
            "format": "json",
        }
        params.update(kwargs)
        res = requests.get(url, params=params)
        data = res.json()
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.errors:
                if form.errors["start_date"]:
                    context["start_date_error"] = form.errors["start_date"]

        period = self.get_period()
        if type(period) is not str:
            start_date = period[0]
            end_date = period[1]
        else:
            start_date = period
            end_date = start_date

        start_date_range = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_date_range = timezone.make_aware(start_date_range)
        end_date_range = datetime.datetime.strptime(end_date, "%Y-%m-%d") + timedelta(
            days=1
        )
        end_date_range = timezone.make_aware(end_date_range)

        # total 'Collectivités":
        context["total_communes"] = Perimeter.objects.filter(
            scale=Perimeter.SCALES.commune, is_obsolete=False
        ).count()
        context["total_epci"] = Perimeter.objects.filter(
            scale=Perimeter.SCALES.epci, is_obsolete=False
        ).count()
        context["total_departments"] = Perimeter.objects.filter(
            scale=Perimeter.SCALES.department, is_obsolete=False
        ).count()
        context["total_regions"] = Perimeter.objects.filter(
            scale=Perimeter.SCALES.region, is_obsolete=False
        ).count()

        matomo_top_aids_pages = self.get_matomo_stats(
            "Actions.getPageUrls",
            date_=f"{start_date},{end_date}",
            **{
                "flat": 1,
                "filter_column": "label",
                # aides/ is optional because the URLs change for portals.
                # Aids slug starts with a 4-letters-or-numbers UUID + `-`.
                # For instance: `/4dc7-passsport/` or `/aides/b68a-accompagner-…`
                "filter_pattern": "^/(aides/)?([a-z0-9]){4}-",
            },
        )[
            :100
        ]  # The `limit` parameter does not look to be effective.

        def aid_from_label(label):
            if label.startswith("/aides/"):
                prefix_length = len("/aides/")
                slug = label[prefix_length:-1]
            else:
                # Aids (slug) at the root for portals.
                slug = label[1:-1]
            # Handle cases where the aid does not exist (outdated database).
            aid = Aid.objects.filter(slug=slug).first()
            # In that case, we fallback to a guessed name from the slug.
            name = slug[5:].replace("-", " ").capitalize()
            return aid if aid is not None else name

        top_aids_pages = [
            {
                "aid_or_name": aid_from_label(page["label"]),
                "nb_visits": page["nb_visits"],
                "nb_uniq_visitors": page.get(
                    "nb_uniq_visitors", page.get("sum_daily_nb_uniq_visitors")
                ),
            }
            for page in matomo_top_aids_pages
        ]
        context["top_aids_pages"] = top_aids_pages

        aids_live_qs = Aid.objects.live()
        matomo_visits_summary = self.get_matomo_stats(
            "VisitsSummary.get", date_=f"{start_date},{end_date}"
        )
        matomo_actions = self.get_matomo_stats(
            "Actions.get", date_=f"{start_date},{end_date}"
        )
        matomo_referrers = self.get_matomo_stats(
            "Referrers.get", date_=f"{start_date},{end_date}"
        )
        matomo_referrers_all = self.get_matomo_stats(
            "Referrers.getAll", date_=f"{start_date},{end_date}"
        )
        tmp_referrers = {}
        nb_referrers_total = 0
        nb_referrers_total_without_search = 0
        for referrer in matomo_referrers_all[:100]:
            nb_visits = referrer["nb_visits"]
            is_search = referrer["label"] == "Keyword not defined"
            if is_search:
                label = "Recherche"
                nb_referrers_total += nb_visits
            else:
                label = referrer["label"]
                nb_referrers_total += nb_visits
                nb_referrers_total_without_search += nb_visits
            tmp_referrers[label] = nb_visits

        referrers = {
            label: (
                nb_visits,
                round(nb_visits / nb_referrers_total * 100, 1),
                round(nb_visits / nb_referrers_total_without_search * 100, 1)
                if label != "Recherche"
                else "-",
            )
            for label, nb_visits in tmp_referrers.items()
        }
        context["referrers"] = referrers

        matomo_last_10_weeks = self.get_matomo_stats(
            "VisitsSummary.get", period="week", date_="last10"
        )
        nb_vu_serie_items = {
            dates[:10]: int(numbers["nb_uniq_visitors"])
            for dates, numbers in matomo_last_10_weeks.items()
        }
        last_10_weeks = [
            datetime.datetime.fromisoformat(week)  # - datetime.timedelta(days=75)
            for week in list(nb_vu_serie_items.keys())
        ]
        week_inscriptions_counts = [
            User.objects.filter(
                date_created__lte=week,
                date_created__gt=week - datetime.timedelta(days=7),
            ).count()
            for week in last_10_weeks
        ]
        context["nb_inscriptions_weeks"] = [
            week.date().isoformat() for week in last_10_weeks
        ]
        context["nb_inscriptions_serie"] = week_inscriptions_counts
        context["nb_inscriptions_with_created_aid_serie"] = [
            User.objects.filter(
                date_created__lte=week,
                date_created__gt=week - datetime.timedelta(days=7),
                aids__isnull=False,
            ).count()
            for week in last_10_weeks
        ]
        context["nb_inscriptions_with_created_project_serie"] = [
            User.objects.filter(
                date_created__lte=week,
                date_created__gt=week - datetime.timedelta(days=7),
                project__isnull=False,
            ).count()
            for week in last_10_weeks
        ]
        context["nb_inscriptions_with_created_alert_serie"] = [
            Alert.objects.filter(validated=True)
            .filter(
                date_created__lte=week,
                date_created__gt=week - datetime.timedelta(days=7),
            )
            .count()
            for week in last_10_weeks
        ]

        week_inscriptions_communes_counts = [
            User.objects.filter(
                date_created__lte=week,
                date_created__gt=week - datetime.timedelta(days=7),
                beneficiary_organization__perimeter__scale=Perimeter.SCALES.commune,
            ).count()
            for week in last_10_weeks
        ]
        context["nb_inscriptions_communes_weeks"] = [
            week.date().isoformat() for week in last_10_weeks
        ]
        context["nb_inscriptions_communes_serie"] = week_inscriptions_communes_counts
        context["nb_inscriptions_communes_with_created_aid_serie"] = [
            User.objects.filter(
                date_created__lte=week,
                date_created__gt=week - datetime.timedelta(days=7),
                beneficiary_organization__perimeter__scale=Perimeter.SCALES.commune,
                aids__isnull=False,
            ).count()
            for week in last_10_weeks
        ]
        context["nb_inscriptions_communes_with_created_project_serie"] = [
            User.objects.filter(
                date_created__lte=week,
                date_created__gt=week - datetime.timedelta(days=7),
                beneficiary_organization__perimeter__scale=Perimeter.SCALES.commune,
                project__isnull=False,
            ).count()
            for week in last_10_weeks
        ]

        context["nb_vu_weeks"] = [week.date().isoformat() for week in last_10_weeks]
        context["nb_vu_serie_values"] = list(nb_vu_serie_items.values())
        context["nb_vu_serie_max"] = max(context["nb_vu_serie_values"])

        # general stats:
        context["nb_beneficiary_accounts"] = User.objects.filter(
            is_beneficiary=True
        ).count()
        context["nb_organizations"] = Organization.objects.count()
        context["nb_projects"] = Project.objects.count()
        context["nb_aids_live"] = aids_live_qs.count()
        context["nb_aids_matching_projects"] = (
            aids_live_qs.exclude(projects=None).distinct().count()
        )
        context["nb_active_financers"] = Backer.objects.has_financed_aids().count()
        context["nb_searchPage"] = SearchPage.objects.count()

        # stats 'Collectivités':
        context["nb_communes"] = (
            Organization.objects.filter(organization_type__contains=["commune"])
            .exclude(perimeter_id__isnull="True")
            .values("city_name", "perimeter_id")
            .distinct()
            .count()
        )
        context["objectif_communes"] = 10000
        context["pourcent_communes"] = round(
            context["nb_communes"] * 100 / context["total_communes"], 1
        )
        context["nb_epci"] = (
            Organization.objects.filter(organization_type__contains=["epci"])
            .exclude(perimeter_id__isnull="True")
            .values("name", "perimeter_id")
            .distinct()
            .count()
        )
        context["objectif_epci"] = 941  # 75%.
        context["pourcent_epci"] = round(
            context["nb_epci"] * 100 / context["total_epci"], 1
        )
        context["nb_departments"] = (
            Organization.objects.filter(organization_type__contains=["department"])
            .exclude(perimeter_id__isnull="True")
            .values("name", "perimeter_id")
            .distinct()
            .count()
        )
        context["nb_regions"] = (
            Organization.objects.filter(organization_type__contains=["region"])
            .exclude(perimeter_id__isnull="True")
            .values("name", "perimeter_id")
            .distinct()
            .count()
        )

        # stats 'Consultation':
        context["nb_viewed_aids"] = AidViewEvent.objects.filter(
            date_created__range=[start_date_range, end_date_range]
        ).count()
        context["nb_visits"] = matomo_visits_summary["nb_visits"]
        context["bounce_rate"] = matomo_visits_summary["bounce_rate"]
        context["avg_time_on_site"] = strftime(
            "%Mm%Ss", gmtime(matomo_visits_summary["avg_time_on_site"])
        )
        context["nb_pageviews"] = matomo_actions["nb_pageviews"]

        # stats 'Acquisition':
        context["nb_direct_visitors"] = matomo_referrers[
            "Referrers_visitorsFromDirectEntry"
        ]
        context["nb_searchEngine_visitors"] = matomo_referrers[
            "Referrers_visitorsFromSearchEngines"
        ]  # noqa
        context["nb_webSite_visitors"] = matomo_referrers[
            "Referrers_visitorsFromWebsites"
        ]
        context["nb_newsletter_visitors"] = matomo_referrers[
            "Referrers_visitorsFromCampaigns"
        ]
        context["nb_socialNetwork_visitors"] = matomo_referrers[
            "Referrers_visitorsFromSocialNetworks"
        ]  # noqa

        # stats 'Engagement':
        context["nb_search_events"] = AidSearchEvent.objects.filter(
            date_created__range=[start_date_range, end_date_range]
        ).count()
        context["nb_alerts_created"] = (
            Alert.objects.filter(validated=True)
            .filter(date_created__range=[start_date_range, end_date_range])
            .count()
        )
        context["nb_aid_contact_click_events"] = AidContactClickEvent.objects.filter(
            date_created__range=[start_date_range, end_date_range]
        ).count()

        # stats for beneficiaries:
        context["nb_beneficiary_accounts_created"] = (
            User.objects.filter(is_beneficiary=True)
            .filter(date_created__range=[start_date_range, end_date_range])
            .count()
        )
        context["nb_beneficiary_organizations"] = (
            Organization.objects.filter(beneficiaries__is_beneficiary=True)
            .filter(date_created__range=[start_date_range, end_date_range])
            .count()
        )
        context["nb_projects_for_period"] = Project.objects.filter(
            date_created__range=[start_date_range, end_date_range]
        ).count()
        context["nb_aids_matching_projects_for_period"] = AidProject.objects.filter(
            date_created__range=[start_date_range, end_date_range]
        ).count()

        # stats for contributors:
        context["nb_contributor_accounts_created"] = (
            User.objects.filter(is_contributor=True)
            .filter(date_created__range=[start_date_range, end_date_range])
            .count()
        )
        context["nb_contributor_organizations"] = (
            Organization.objects.filter(beneficiaries__is_contributor=True)
            .filter(date_created__range=[start_date_range, end_date_range])
            .count()
        )
        context["nb_aids_live_for_period"] = aids_live_qs.filter(
            date_created__range=[start_date_range, end_date_range]
        ).count()

        return context


class UsersStatsView(SuperUserRequiredMixin, FormMixin, ListView):
    template_name = "stats/users_stats.html"
    form_class = StatSearchForm
    context_object_name = "users"
    paginate_by = 50
    paginator_class = AidPaginator

    def get_period(self):

        period = timezone.now().strftime("%Y-%m-%d")

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                if form.cleaned_data["end_date"]:
                    end_date = form.cleaned_data["end_date"]
                else:
                    end_date = start_date

                start_date = start_date.strftime("%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
                period = start_date.split() + end_date.split()

        return period

    def get_queryset(self):
        """Return the list of users to display."""

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.errors:
                if form.errors["start_date"]:
                    context["start_date_error"] = form.errors["start_date"]  # noqa

        period = self.get_period()
        if type(period) is not str:
            start_date = period[0]
            end_date = period[1]
        else:
            start_date = period
            end_date = start_date

        start_date_range = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_date_range = timezone.make_aware(start_date_range)
        end_date_range = datetime.datetime.strptime(end_date, "%Y-%m-%d") + timedelta(
            days=1
        )
        end_date_range = timezone.make_aware(end_date_range)

        users = (
            User.objects.filter(date_created__range=[start_date_range, end_date_range])
            .select_related("beneficiary_organization")
            .order_by("-date_created")
        )

        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # general stats:
        context["nb_beneficiaries_and_contributors"] = (
            User.objects.filter(is_beneficiary=True).filter(is_contributor=True).count()
        )
        context["nb_beneficiaries_only"] = (
            User.objects.filter(is_beneficiary=True)
            .exclude(is_contributor=True)
            .count()
        )
        context["nb_contributors_only"] = (
            User.objects.filter(is_contributor=True)
            .exclude(is_beneficiary=True)
            .count()
        )
        context["nb_users"] = User.objects.all().count()

        return context


class CartoStatsView(SuperUserRequiredMixin, TemplateView):
    template_name = "stats/carto_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["regions_geojson"] = (
            Path(".").resolve() / "static" / "geojson" / "regions-1000m.geojson"
        ).read_text()

        # Counts by region.
        regions = Perimeter.objects.filter(
            scale=Perimeter.SCALES.region, is_obsolete=False
        )
        regions_org_counts = {}
        regions_org_communes_max = 0
        for region in regions:
            communes_count = (
                region.organization_region.filter(organization_type=["commune"])
                .distinct()
                .values("id")
                .count()
            )
            regions_org_communes_max = max(regions_org_communes_max, communes_count)
            epcis_count = (
                region.organization_region.filter(organization_type=["epci"])
                .distinct()
                .values("id")
                .count()
            )
            regions_org_counts[region.code] = {
                "name": region.name,
                "communes_count": communes_count,
                "epcis_count": epcis_count,
            }
        context["regions_org_communes_max"] = regions_org_communes_max
        context["regions_org_counts"] = json.dumps(
            regions_org_counts, cls=DjangoJSONEncoder
        )

        # Counts by department.
        departments = Perimeter.objects.departments()
        departments_org_counts = {}
        departments_codes = []
        for department in departments:
            departments_codes.append(department.code)
            communes_count = (
                department.organization_department.filter(
                    organization_type=["commune"],
                    perimeter__scale=Perimeter.SCALES.commune,
                    perimeter__is_obsolete=False,
                )
                .distinct()
                .values("id")
                .count()
            )
            epcis_count = (
                department.organization_department.filter(
                    organization_type=["epci"],
                    perimeter__scale=Perimeter.SCALES.epci,
                    perimeter__is_obsolete=False,
                )
                .distinct()
                .values("id")
                .count()
            )
            total_communes_count = NB_COMMUNES_PAR_DEPARTEMENT_2022[department.code]
            percentage_communes = round(communes_count * 100 / total_communes_count, 1)
            departments_org_counts[department.code] = {
                "name": department.name,
                "communes_count": communes_count,
                "percentage_communes": percentage_communes,
                "epcis_count": epcis_count,
            }
        context["departments_codes"] = departments_codes
        # We do not attempt to get the max of percentage_communes here
        # because some departments (like Guadeloupe) have a very high
        # percentage and are hiding small differences across metropolitan
        # departments…
        # Once homogenized, it is possible to use the logic for regions here.
        context["departments_org_communes_max"] = DEPARTMENTS_ORG_COMMUNES_MAX
        context["departments_org_counts"] = json.dumps(
            departments_org_counts, cls=DjangoJSONEncoder
        )

        # Organizations with commune as a perimeter.
        organizations_communes = (
            Organization.objects.filter(
                perimeter__scale=Perimeter.SCALES.commune,
                perimeter__is_obsolete=False,
                organization_type=["commune"],
            )
            .annotate(projects_count=Count("project", distinct=True))
            .values(
                "name",
                "date_created",
                "projects_count",
                "perimeter__code",
                "perimeter__name",
                "user__email",
                "organization_type",
            )
        )

        def get_age(date_):
            now = datetime.datetime.now(timezone.utc)
            if now - datetime.timedelta(days=30) < date_:
                return 3
            if now - datetime.timedelta(days=90) < date_:
                return 2
            else:
                return 1

        communes_with_org = defaultdict(list)
        for organization in organizations_communes:
            key = f"{organization['perimeter__code']}-{organization['perimeter__name']}"
            content = {
                "organization_name": organization["name"],
                "user_email": organization["user__email"],
                "projects_count": organization["projects_count"],
                "date_created": organization["date_created"],
                "age": get_age(organization["date_created"]),
            }
            if key in communes_with_org:
                already_exists = False
                for commune in communes_with_org[key]:
                    if commune["organization_name"] == organization["name"]:
                        already_exists = True
                        commune[
                            "user_email"
                        ] = f'{commune["user_email"]}, {organization["user__email"]}'
                if not already_exists:
                    communes_with_org[key].append(content)
            else:
                communes_with_org[key].append(content)
        context["communes_with_org"] = json.dumps(
            communes_with_org, cls=DjangoJSONEncoder
        )

        # Organizations with EPCI as a perimeter.
        organizations_epcis = (
            Organization.objects.filter(
                perimeter__scale=Perimeter.SCALES.epci,
                perimeter__is_obsolete=False,
                organization_type=["epci"],
            )
            .annotate(projects_count=Count("project", distinct=True))
            .values(
                "name",
                "date_created",
                "projects_count",
                "perimeter__id",
                "user__email",
            )
        )
        epcis_with_org = defaultdict(list)
        communes_perimeters = {}
        for organization in organizations_epcis:
            # Cache commune perimeters for a given perimeter id.
            perimeter_id = organization["perimeter__id"]
            if perimeter_id in communes_perimeters:
                perimeters = communes_perimeters[perimeter_id]
            else:
                perimeters = get_all_related_perimeters(
                    perimeter_id,
                    direction="down",
                    scale=Perimeter.SCALES.commune,
                    values=["code", "name"],
                )
                communes_perimeters[perimeter_id] = perimeters

            for perimeter in perimeters:
                key = f"{perimeter['code']}-{perimeter['name']}"
                content = {
                    "organization_name": organization["name"],
                    "user_email": organization["user__email"],
                    "projects_count": organization["projects_count"],
                    "date_created": organization["date_created"],
                    "age": 4,
                }
                if key in epcis_with_org:
                    already_exists = False
                    for epci in epcis_with_org[key]:
                        if epci["organization_name"] == organization["name"]:
                            already_exists = True
                            epci[
                                "user_email"
                            ] = f'{epci["user_email"]}, {organization["user__email"]}'
                            epci["projects_count"] = (
                                epci["projects_count"] + organization["projects_count"]
                            )
                    if not already_exists:
                        epcis_with_org[key].append(content)
                else:
                    epcis_with_org[key].append(content)

        context["epcis_with_org"] = json.dumps(epcis_with_org, cls=DjangoJSONEncoder)
        return context


class ProjectsStatsView(SuperUserRequiredMixin, FormMixin, ListView):
    template_name = "stats/projects_stats.html"
    form_class = StatSearchForm
    context_object_name = "projects"
    paginate_by = 50
    paginator_class = AidPaginator

    def get_period(self):

        period = timezone.now().strftime("%Y-%m-%d")

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                if form.cleaned_data["end_date"]:
                    end_date = form.cleaned_data["end_date"]
                else:
                    end_date = start_date

                start_date = start_date.strftime("%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
                period = start_date.split() + end_date.split()

        return period

    def get_queryset(self):
        """Return the list of users to display."""

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.errors:
                if form.errors["start_date"]:
                    context["start_date_error"] = form.errors["start_date"]  # noqa

        period = self.get_period()
        if type(period) is not str:
            start_date = period[0]
            end_date = period[1]
        else:
            start_date = period
            end_date = start_date

        start_date_range = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_date_range = timezone.make_aware(start_date_range)
        end_date_range = datetime.datetime.strptime(end_date, "%Y-%m-%d") + timedelta(
            days=1
        )
        end_date_range = timezone.make_aware(end_date_range)

        projects = (
            Project.objects.filter(
                date_created__range=[start_date_range, end_date_range]
            )
            .prefetch_related("organizations")
            .prefetch_related("aid_set")
            .order_by("-date_created")
        )

        return projects


class OrganizationsStatsView(SuperUserRequiredMixin, FormMixin, ListView):
    template_name = "stats/organizations_stats.html"
    form_class = StatSearchForm
    context_object_name = "organizations"
    paginate_by = 50
    paginator_class = AidPaginator

    def get_period(self):

        period = timezone.now().strftime("%Y-%m-%d")

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                if form.cleaned_data["end_date"]:
                    end_date = form.cleaned_data["end_date"]
                else:
                    end_date = start_date

                start_date = start_date.strftime("%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
                period = start_date.split() + end_date.split()

        return period

    def get_queryset(self):
        """Return the list of users to display."""

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.errors:
                if form.errors["start_date"]:
                    context["start_date_error"] = form.errors["start_date"]  # noqa

        period = self.get_period()
        if type(period) is not str:
            start_date = period[0]
            end_date = period[1]
        else:
            start_date = period
            end_date = start_date

        start_date_range = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_date_range = timezone.make_aware(start_date_range)
        end_date_range = datetime.datetime.strptime(end_date, "%Y-%m-%d") + timedelta(
            days=1
        )
        end_date_range = timezone.make_aware(end_date_range)

        organizations = (
            Organization.objects.filter(
                date_created__range=[start_date_range, end_date_range]
            )
            .prefetch_related("beneficiaries")
            .select_related("perimeter")
            .order_by("-date_created")
        )

        return organizations

    def get_context_data(self, **kwargs):
        """
        Statistics by organization type, with some deduplication:
        - Exclude orgs without organization_type or perimeter
        - Group "commune" type orgs that have the same city_name and perimeter_id
          (eg "Mairie de Vaugrineuse" and "Ville de Vaugrineuse" will be counted once
          provided they have the same perimeter_id)
        - Similarly, group other types of organization by their name and perimeter_id
        """
        context = super().get_context_data(**kwargs)

        communes_count = (
            Organization.objects.filter(organization_type__contains=["commune"])
            .exclude(perimeter_id__isnull="True")
            .values("organization_type", "city_name", "perimeter_id")
            .distinct()
            .count()
        )

        all_organizations_types = {"commune": communes_count}

        other_organizations = (
            Organization.objects.exclude(organization_type__contains=["commune"])
            .exclude(organization_type__isnull=True)
            .exclude(perimeter_id__isnull="True")
            .values("organization_type", "name", "perimeter_id")
            .distinct()
            .order_by("organization_type")
        )

        for org in other_organizations:
            org_type = org["organization_type"][0]
            if org_type is not None:
                if org_type not in all_organizations_types:
                    all_organizations_types[org_type] = 1
                else:
                    all_organizations_types[org_type] += 1

        context["all_organizations_types"] = all_organizations_types
        context["total_organizations"] = sum(all_organizations_types.values())

        return context
