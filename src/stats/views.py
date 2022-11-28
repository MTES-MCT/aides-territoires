import json
import requests
import datetime
from collections import defaultdict
from datetime import date, timedelta
from time import strftime, gmtime
from pathlib import Path

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from django.db.models import Count, Q, Sum
from django.views.generic.edit import FormMixin

from accounts.mixins import SuperUserRequiredMixin
from accounts.models import User, UserLastConnexion
from aids.constants import AUDIENCES_ALL
from aids.models import Aid, AidProject
from aids.views import AidPaginator
from alerts.models import Alert
from backers.models import Backer
from geofr.models import Perimeter
from geofr.utils import get_all_related_perimeters
from organizations.models import Organization
from projects.models import Project
from search.models import SearchPage
from stats.forms import StatSearchForm
from stats.models import (
    AidViewEvent,
    Event,
    AidSearchEvent,
    AidApplicationUrlClickEvent,
    AidContactClickEvent,
    AidOriginUrlClickEvent,
)

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


OBJECTIF_COMMUNES = 10000  # of 35049.
OBJECTIF_EPCI = 941  # 75% of 1255.


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


class MatomoMixin:
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


class DashboardBaseView(MatomoMixin, SuperUserRequiredMixin, FormMixin):
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

    def get_context_dates(self, context, **kwargs):
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
        context["start_date"] = start_date
        context["end_date"] = end_date
        context["start_date_range"] = start_date_range
        context["end_date_range"] = end_date_range
        return context

    def get_context_stats(self, context, **kwargs):
        # General stats.
        aids_live_qs = Aid.objects.live()
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

        # Total 'Collectivités'.
        context["total_communes"] = Perimeter.objects.filter(
            scale=Perimeter.SCALES.commune, is_obsolete=False
        ).count()
        context["total_epci"] = Perimeter.objects.filter(
            scale=Perimeter.SCALES.epci, is_obsolete=False
        ).count()

        # Stats 'Collectivités'.
        context["nb_communes"] = (
            Organization.objects.filter(
                organization_type=["commune"],
                perimeter__scale=Perimeter.SCALES.commune,
                perimeter__is_obsolete=False,
            )
            .exclude(perimeter_id__isnull="True")
            .order_by("perimeter")
            .distinct("perimeter")
            .count()
        )
        context["objectif_communes"] = OBJECTIF_COMMUNES
        context["pourcent_communes"] = round(
            context["nb_communes"] * 100 / context["total_communes"], 1
        )
        context["nb_extra_communes"] = max(
            context["nb_communes"] - context["objectif_communes"], 0
        )

        context["nb_epci"] = (
            Organization.objects.filter(
                organization_type=["epci"],
                perimeter__scale=Perimeter.SCALES.epci,
                perimeter__is_obsolete=False,
            )
            .exclude(perimeter_id__isnull="True")
            .order_by("perimeter")
            .distinct("perimeter")
            .count()
        )
        context["objectif_epci"] = OBJECTIF_EPCI
        context["pourcent_epci"] = round(
            context["nb_epci"] * 100 / context["total_epci"], 1
        )
        context["nb_extra_epci"] = max(context["nb_epci"] - context["objectif_epci"], 0)

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_context_dates(context, **kwargs)
        context = self.get_context_stats(context, **kwargs)
        return context


class DashboardConsultationView(DashboardBaseView, TemplateView):
    template_name = "stats/dashboard_consultation.html"
    form_class = StatSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = context["start_date"]
        end_date = context["end_date"]
        start_date_range = context["start_date_range"]
        end_date_range = context["end_date_range"]

        matomo_visits_summary = self.get_matomo_stats(
            "VisitsSummary.get", date_=f"{start_date},{end_date}"
        )
        matomo_actions = self.get_matomo_stats(
            "Actions.get", date_=f"{start_date},{end_date}"
        )
        matomo_last_10_weeks = self.get_matomo_stats(
            "VisitsSummary.get", period="week", date_="last10"
        )
        nb_vu_serie_items = {
            dates[:10]: int(numbers["nb_uniq_visitors"])
            for dates, numbers in matomo_last_10_weeks.items()
        }
        last_10_weeks = [
            datetime.datetime.fromisoformat(week)
            for week in list(nb_vu_serie_items.keys())
        ]
        week_inscriptions_counts = []
        for week in last_10_weeks:
            users = User.objects.filter(
                date_created__range=[week - datetime.timedelta(days=7), week],
            ).annotate(
                aids_subscription_count=Count(
                    "aids", filter=Q(aids__isnull=False), distinct=True
                )
            )
            week_inscriptions_counts.append(len(users))
        context["nb_inscriptions_weeks"] = [
            week.date().isoformat() for week in last_10_weeks
        ]
        context["nb_inscriptions_serie"] = week_inscriptions_counts
        context["nb_inscriptions_with_created_alert_serie"] = [
            Alert.objects.filter(validated=True)
            .filter(
                date_created__range=[week - datetime.timedelta(days=7), week],
            )
            .count()
            for week in last_10_weeks
        ]
        context["nb_vu_weeks"] = [week.date().isoformat() for week in last_10_weeks]
        context["nb_vu_serie_values"] = list(nb_vu_serie_items.values())
        context["nb_vu_serie_max"] = max(context["nb_vu_serie_values"])

        # stats 'Consultation':
        context["nb_viewed_aids"] = (
            AidViewEvent.objects.filter(
                date_created__range=[start_date_range, end_date_range]
            )
            .exclude(source="api")
            .count()
        )
        context["nb_different_viewed_aids"] = (
            AidViewEvent.objects.filter(
                date_created__range=[start_date_range, end_date_range]
            )
            .exclude(source="api")
            .distinct("aid")
            .count()
        )
        context["nb_visits"] = matomo_visits_summary["nb_visits"]
        context["bounce_rate"] = matomo_visits_summary["bounce_rate"]
        context["avg_time_on_site"] = strftime(
            "%Mm%Ss", gmtime(matomo_visits_summary["avg_time_on_site"])
        )
        context["nb_pageviews"] = matomo_actions["nb_pageviews"]

        context["consultation_selected"] = True
        return context


class DashboardAcquisitionView(DashboardBaseView, TemplateView):
    template_name = "stats/dashboard_acquisition.html"
    form_class = StatSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = context["start_date"]
        end_date = context["end_date"]
        start_date_range = context["start_date_range"]
        end_date_range = context["end_date_range"]

        matomo_referrers = self.get_matomo_stats(
            "Referrers.get", date_=f"{start_date},{end_date}"
        )

        # Display the table of referrers for the given range.
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

        # Display the graph+table of new users for the given range.
        user_inscriptions = (
            User.objects.filter(
                date_created__range=[start_date_range, end_date_range],
            )
            .order_by("-date_created")
            .values(
                "email",
                "first_name",
                "last_name",
                "date_created",
                "organization__name",
                "organization__organization_type",
            )
        )
        org_type_to_display_name = dict(AUDIENCES_ALL)
        user_inscriptions_by_date = defaultdict(int)
        for user_inscription in user_inscriptions:
            user_inscriptions_by_date[
                user_inscription["date_created"].date().strftime("%Y-%m-%d")
            ] += 1
            org_type = user_inscription["organization__organization_type"]
            if org_type:
                user_inscription["organization_type"] = org_type_to_display_name.get(
                    org_type[0]
                )
        context["user_inscriptions"] = user_inscriptions

        current_date = start_date_range
        nb_user_days = []
        nb_user_inscriptions = []
        while current_date < end_date_range:
            date_ = current_date.date().strftime("%Y-%m-%d")
            nb_user_days.append(date_)
            nb_user_inscriptions.append(user_inscriptions_by_date.get(date_, 0))
            current_date += timedelta(days=1)
        context["nb_user_days"] = nb_user_days
        context["nb_user_inscriptions_serie"] = nb_user_inscriptions

        # stats 'Acquisition':
        context["nb_direct_visitors"] = matomo_referrers[
            "Referrers_visitorsFromDirectEntry"
        ]
        context["nb_searchEngine_visitors"] = matomo_referrers[
            "Referrers_visitorsFromSearchEngines"
        ]
        context["nb_webSite_visitors"] = matomo_referrers[
            "Referrers_visitorsFromWebsites"
        ]
        context["nb_newsletter_visitors"] = matomo_referrers[
            "Referrers_visitorsFromCampaigns"
        ]
        context["nb_socialNetwork_visitors"] = matomo_referrers[
            "Referrers_visitorsFromSocialNetworks"
        ]

        context["acquisition_selected"] = True
        return context


class DashboardEngagementView(DashboardBaseView, TemplateView):
    template_name = "stats/dashboard_engagement.html"
    form_class = StatSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = context["start_date"]
        end_date = context["end_date"]
        start_date_range = context["start_date_range"]
        end_date_range = context["end_date_range"]

        NB_OF_TOP_AIDS = 100

        matomo_top_aids_pages = self.get_matomo_stats(
            "Actions.getPageUrls",
            date_=f"{start_date},{end_date}",
            **{
                "flat": 1,
                "filter_column": "label",
                # We put the limit to 130% to be sure that the number of wanted
                # results are available in the table (minus portals duplicates).
                "filter_limit": NB_OF_TOP_AIDS * 1.3,
                # aides/ is optional because the URLs change for portals.
                # Aids slug starts with a 4-letters-or-numbers UUID + `-`.
                # For instance: `/4dc7-passsport/` or `/aides/b68a-accompagner-…`
                "filter_pattern": "^/(aides/)?([a-z0-9]){4}-",
            },
        )

        def get_slug(label):
            if label.startswith("/aides/"):
                prefix_length = len("/aides/")
                return label[prefix_length:-1]
            else:
                # Aids (slug) at the root for portals.
                return label[1:-1]

        # It is a bit ugly but we try to get all Aids in one query,
        # hence the slug dance.
        slugs_pages = {}
        for page in matomo_top_aids_pages:
            slug = get_slug(page["label"])
            if slug in slugs_pages:
                # In case we already have an entry, we add up counts to
                # sum all visits either from portals or main.
                try:
                    slugs_pages[slug]["nb_uniq_visitors"] += page["nb_uniq_visitors"]
                except KeyError:
                    pass
                try:
                    slugs_pages[slug]["sum_daily_nb_uniq_visitors"] += page[
                        "sum_daily_nb_uniq_visitors"
                    ]
                except KeyError:
                    pass
                continue
            slugs_pages[slug] = page

        aids = (
            Aid.objects.filter(
                # We cannot use slug__in because Matomo is returning truncated slugs!
                Q(
                    *[("slug__startswith", slug) for slug in slugs_pages.keys()],
                    _connector=Q.OR,
                )
            )
            .select_related("perimeter")
            .prefetch_related("financers")
            .annotate(
                aidproject_count=Count(
                    "aidproject",
                    filter=Q(date_created__range=[start_date_range, end_date_range]),
                    distinct=True,
                )
            )
        )
        slugs_aids = {aid.slug: aid for aid in aids}
        top_aids_pages = []
        for slug, page in slugs_pages.items():
            aid_stats = {
                # Matomo “doesn't process unique visitors across the full period.”
                # so we multiply their daily value with the number of days for
                # the given period, if the range is more that one day. Otherwise,
                # the `nb_uniq_visitors` key is present in the page result.
                "nb_uniq_visitors": page.get("nb_uniq_visitors")
                or page["sum_daily_nb_uniq_visitors"]
                * (end_date_range - start_date_range).days,
            }
            aid = slugs_aids.get(slug)
            if aid is None:  # Recent aid, not yet in local database.
                # In that case, we fallback to a guessed name from the slug.
                aid_stats["guessed_name"] = slug[5:].replace("-", " ").capitalize()
            else:
                # Adding extra annotate() turns the query into a monster,
                # so we perform additional but smaller ones here.
                aid.contact_clicks_count = aid.aidcontactclickevent_set.filter(
                    date_created__range=[start_date_range, end_date_range]
                ).count()
                aid.origin_clicks_count = aid.aidoriginurlclickevent_set.filter(
                    date_created__range=[start_date_range, end_date_range]
                ).count()
                aid.application_clicks_count = (
                    aid.aidapplicationurlclickevent_set.filter(
                        date_created__range=[start_date_range, end_date_range]
                    ).count()
                )
                aid.all_clicks_count = (
                    aid.contact_clicks_count
                    + aid.origin_clicks_count
                    + aid.application_clicks_count
                )
                # We need the conversion value here (vs. `percent_display`) because
                # we have to pass it raw to the triaging function of the JS table.
                aid.conversion_value = round(
                    100 * aid.all_clicks_count / aid_stats["nb_uniq_visitors"], 3
                )
                aid_stats["aid"] = aid
            top_aids_pages.append(aid_stats)

        context["top_aids_pages"] = sorted(
            top_aids_pages, key=lambda a: a["nb_uniq_visitors"], reverse=True
        )[:NB_OF_TOP_AIDS]

        matomo_last_10_weeks = self.get_matomo_stats(
            "VisitsSummary.get", period="week", date_="last10"
        )
        nb_vu_serie_items = {
            dates[:10]: int(numbers["nb_uniq_visitors"])
            for dates, numbers in matomo_last_10_weeks.items()
        }
        last_10_weeks = [
            datetime.datetime.fromisoformat(week)
            for week in list(nb_vu_serie_items.keys())
        ]
        week_inscriptions_counts = []
        nb_inscriptions_with_created_aid_serie = []
        nb_inscriptions_with_created_project_serie = []
        for week in last_10_weeks:
            users = (
                User.objects.filter(
                    date_created__range=[week - datetime.timedelta(days=7), week],
                )
                .annotate(
                    aids_subscription_count=Count(
                        "aids", filter=Q(aids__isnull=False), distinct=True
                    )
                )
                .annotate(
                    project_subscription_count=Count(
                        "project", filter=Q(project__isnull=False), distinct=True
                    )
                )
            )
            week_inscriptions_counts.append(len(users))
            user_aids_subscription_counts = sum(
                user.aids_subscription_count for user in users
            )
            user_project_subscription_counts = sum(
                user.project_subscription_count for user in users
            )
            nb_inscriptions_with_created_aid_serie.append(user_aids_subscription_counts)
            nb_inscriptions_with_created_project_serie.append(
                user_project_subscription_counts
            )

        context["nb_inscriptions_weeks"] = [
            week.date().isoformat() for week in last_10_weeks
        ]
        context["nb_inscriptions_serie"] = week_inscriptions_counts
        context[
            "nb_inscriptions_with_created_aid_serie"
        ] = nb_inscriptions_with_created_aid_serie
        context[
            "nb_inscriptions_with_created_project_serie"
        ] = nb_inscriptions_with_created_project_serie
        context["nb_inscriptions_with_created_alert_serie"] = [
            Alert.objects.filter(validated=True)
            .filter(
                date_created__range=[week - datetime.timedelta(days=7), week],
            )
            .count()
            for week in last_10_weeks
        ]

        today = date.today()

        def first_of_month_between(start, end):
            dt = start
            dates = []

            while dt < end:
                if not dt.month % 12:
                    dt = date(dt.year + 1, 1, 1)
                else:
                    dt = date(dt.year, dt.month + 1, 1)
                dates.append(dt.isoformat())
            return dates

        # We compute the start/end date to start 6 months ago but
        # we also want to avoid the current/in progress month so
        # we move the range 30 days ago.
        last_6_months = first_of_month_between(
            today - timedelta(days=183 + 30), today - timedelta(days=30)
        )

        def neighborhood(iterable, last=None):
            """
            Yield the (current, next) items given an iterable.
            You can specify a `last` item for bounds.
            """
            iterator = iter(iterable)
            current = next(iterator)  # Throws StopIteration if empty.
            for next_ in iterator:
                yield (current, next_)
                current = next_
            yield (current, last)

        context["nb_activite_months"] = last_6_months[:-1]
        context["nb_activite_serie"] = [
            UserLastConnexion.objects.filter(
                last_connexion__range=[month, next_month],
                user__is_superuser=False,
            )
            .order_by("user__pk")
            .distinct("user__pk")
            .count()
            for (month, next_month) in neighborhood(last_6_months)
            if next_month is not None
        ]
        context["nb_activite_communes_serie"] = [
            UserLastConnexion.objects.filter(
                last_connexion__range=[month, next_month],
                user__is_superuser=False,
                user__organization__perimeter__scale=Perimeter.SCALES.commune,
                user__beneficiary_organization__organization_type=["commune"],
            )
            .order_by("user__pk")
            .distinct("user__pk")
            .count()
            for (month, next_month) in neighborhood(last_6_months)
            if next_month is not None
        ]
        context["nb_activite_epci_serie"] = [
            UserLastConnexion.objects.filter(
                last_connexion__range=[month, next_month],
                user__is_superuser=False,
                user__organization__perimeter__scale=Perimeter.SCALES.epci,
                user__beneficiary_organization__organization_type=["epci"],
            )
            .order_by("user__pk")
            .distinct("user__pk")
            .count()
            for (month, next_month) in neighborhood(last_6_months)
            if next_month is not None
        ]

        # stats 'Engagement':
        context["nb_active_users"] = (
            UserLastConnexion.objects.filter(
                last_connexion__range=[start_date_range, end_date_range],
                user__is_superuser=False,
            )
            .order_by("user__pk")
            .distinct("user__pk")
            .count()
        )
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
        context[
            "nb_aid_origin_url_clicks_count"
        ] = AidOriginUrlClickEvent.objects.filter(
            date_created__range=[start_date_range, end_date_range]
        ).count()
        context[
            "nb_aid_application_url_clicks_count"
        ] = AidApplicationUrlClickEvent.objects.filter(
            date_created__range=[start_date_range, end_date_range]
        ).count()

        context["engagement_selected"] = True
        return context


class DashboardPorteursView(DashboardBaseView, TemplateView):
    template_name = "stats/dashboard_porteurs.html"
    form_class = StatSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date_range = context["start_date_range"]
        end_date_range = context["end_date_range"]

        matomo_last_10_weeks = self.get_matomo_stats(
            "VisitsSummary.get", period="week", date_="last10"
        )
        nb_vu_serie_items = {
            dates[:10]: int(numbers["nb_uniq_visitors"])
            for dates, numbers in matomo_last_10_weeks.items()
        }
        last_10_weeks = [
            datetime.datetime.fromisoformat(week)
            for week in list(nb_vu_serie_items.keys())
        ]
        week_inscriptions_communes_counts = []
        week_inscriptions_epcis_counts = []
        nb_inscriptions_with_created_aid_communes_serie = []
        nb_inscriptions_with_created_aid_epcis_serie = []
        nb_inscriptions_with_created_project_communes_serie = []
        nb_inscriptions_with_created_project_epcis_serie = []
        commune_scale = Perimeter.SCALES.commune
        epci_scale = Perimeter.SCALES.epci
        for week in last_10_weeks:
            users = (
                User.objects.filter(
                    date_created__range=[week - datetime.timedelta(days=7), week],
                )
                .annotate(
                    aids_commune_subscription_count=Count(
                        "aids",
                        filter=Q(
                            aids__isnull=False,
                            beneficiary_organization__perimeter__scale=commune_scale,
                        ),
                        distinct=True,
                    )
                )
                .annotate(
                    aids_epci_subscription_count=Count(
                        "aids",
                        filter=Q(
                            aids__isnull=False,
                            beneficiary_organization__perimeter__scale=epci_scale,
                        ),
                        distinct=True,
                    )
                )
                .annotate(
                    project_commune_subscription_count=Count(
                        "project",
                        filter=Q(
                            project__isnull=False,
                            beneficiary_organization__perimeter__scale=commune_scale,
                        ),
                        distinct=True,
                    )
                )
                .annotate(
                    project_epci_subscription_count=Count(
                        "project",
                        filter=Q(
                            project__isnull=False,
                            beneficiary_organization__perimeter__scale=epci_scale,
                        ),
                        distinct=True,
                    )
                )
            )
            week_inscriptions_communes_counts.append(
                users.filter(
                    beneficiary_organization__perimeter__scale=commune_scale
                ).count()
            )
            week_inscriptions_epcis_counts.append(
                users.filter(
                    beneficiary_organization__perimeter__scale=epci_scale
                ).count()
            )
            user_aids_commune_subscription_counts = sum(
                user.aids_commune_subscription_count for user in users
            )
            user_aids_epci_subscription_counts = sum(
                user.aids_epci_subscription_count for user in users
            )
            user_project_commune_subscription_counts = sum(
                user.project_commune_subscription_count for user in users
            )
            user_project_epci_subscription_counts = sum(
                user.project_epci_subscription_count for user in users
            )
            nb_inscriptions_with_created_aid_communes_serie.append(
                user_aids_commune_subscription_counts
            )
            nb_inscriptions_with_created_project_communes_serie.append(
                user_project_commune_subscription_counts
            )
            nb_inscriptions_with_created_aid_epcis_serie.append(
                user_aids_epci_subscription_counts
            )
            nb_inscriptions_with_created_project_epcis_serie.append(
                user_project_epci_subscription_counts
            )

        context["nb_inscriptions_weeks"] = [
            week.date().isoformat() for week in last_10_weeks
        ]

        context["nb_inscriptions_communes_serie"] = week_inscriptions_communes_counts
        context[
            "nb_inscriptions_communes_with_created_aid_serie"
        ] = nb_inscriptions_with_created_aid_communes_serie
        context[
            "nb_inscriptions_communes_with_created_project_serie"
        ] = nb_inscriptions_with_created_project_communes_serie

        context["nb_inscriptions_epcis_serie"] = week_inscriptions_epcis_counts
        context[
            "nb_inscriptions_epcis_with_created_aid_serie"
        ] = nb_inscriptions_with_created_aid_epcis_serie
        context[
            "nb_inscriptions_epcis_with_created_project_serie"
        ] = nb_inscriptions_with_created_project_epcis_serie

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
        context["nb_aids_live_for_period"] = (
            Aid.objects.live()
            .filter(date_created__range=[start_date_range, end_date_range])
            .count()
        )

        context["porteurs_selected"] = True
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
                region.organization_region.filter(
                    organization_type=["commune"],
                    perimeter__scale=Perimeter.SCALES.commune,
                    perimeter__is_obsolete=False,
                )
                .exclude(perimeter_id__isnull="True")
                .order_by("perimeter")
                .distinct("perimeter")
                .values("id")
                .count()
            )
            regions_org_communes_max = max(regions_org_communes_max, communes_count)
            epcis_count = (
                region.organization_region.filter(
                    organization_type=["epci"],
                    perimeter__scale=Perimeter.SCALES.epci,
                    perimeter__is_obsolete=False,
                )
                .exclude(perimeter_id__isnull="True")
                .order_by("perimeter")
                .distinct("perimeter")
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
                .exclude(perimeter_id__isnull="True")
                .order_by("perimeter")
                .distinct("perimeter")
                .values("id")
                .count()
            )
            epcis_count = (
                department.organization_department.filter(
                    organization_type=["epci"],
                    perimeter__scale=Perimeter.SCALES.epci,
                    perimeter__is_obsolete=False,
                )
                .exclude(perimeter_id__isnull="True")
                .order_by("perimeter")
                .distinct("perimeter")
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
