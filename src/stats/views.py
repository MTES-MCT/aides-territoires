import json
import requests
import datetime
from datetime import timedelta
from time import strftime, gmtime
from pathlib import Path

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from django.db.models import Sum
from django.views.generic.edit import FormMixin

from aids.models import Aid, AidProject
from accounts.models import User
from backers.models import Backer
from geofr.models import Perimeter
from stats.models import AidViewEvent, Event, AidSearchEvent, AidContactClickEvent
from organizations.models import Organization
from projects.models import Project
from search.models import SearchPage
from alerts.models import Alert

from stats.forms import StatSearchForm
from accounts.mixins import SuperUserRequiredMixin
from aids.views import AidPaginator


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

    def get_matomo_stats(self, method, start_date, end_date):
        """
        Here we want to get the stats from Matomo.
        """

        url = "https://stats.data.gouv.fr/"

        params = {
            "idSite": settings.MATOMO_SITE_ID,
            "module": "API",
            "method": method,
            "period": "range",
            "date": f"{start_date},{end_date}",
            "format": "json",
        }
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

        aids_live_qs = Aid.objects.live()
        matomo_visits_summary = self.get_matomo_stats(
            "VisitsSummary.get", start_date, end_date
        )
        matomo_actions = self.get_matomo_stats("Actions.get", start_date, end_date)
        matomo_referrers = self.get_matomo_stats("Referrers.get", start_date, end_date)

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
        context["nb_epci"] = (
            Organization.objects.filter(organization_type__contains=["epci"])
            .exclude(perimeter_id__isnull="True")
            .values("name", "perimeter_id")
            .distinct()
            .count()
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

        # stats 'Consultation':
        context["nb_viewed_aids"] = AidViewEvent.objects.filter(
            date_created__range=[start_date_range, end_date_range]
        ).count()
        # la valeur "nb_uniq_visitors" n'est pas renvoyée quand period=range
        if "nb_uniq_visitors" in matomo_visits_summary:
            context["nb_uniq_visitors"] = matomo_visits_summary["nb_uniq_visitors"]
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
        regions_org_count = {}
        for region in regions:
            regions_org_count[region.name] = region.organization_region.values(
                "id"
            ).count()
        context["regions_org_max"] = max(regions_org_count.values())
        context["regions_org_count"] = json.dumps(
            regions_org_count, cls=DjangoJSONEncoder
        )

        # Counts by department.
        departments = Perimeter.objects.filter(
            scale=Perimeter.SCALES.department, is_obsolete=False
        )
        departments_org_count = {}
        for department in departments:
            departments_org_count[
                department.name
            ] = department.organization_department.values("id").count()
        context["departments_org_max"] = max(departments_org_count.values())
        context["departments_org_count"] = json.dumps(
            departments_org_count, cls=DjangoJSONEncoder
        )

        # Communes with a perimeter.
        communes = (
            Perimeter.objects.filter(
                scale=Perimeter.SCALES.commune,
                is_obsolete=False,
                organization__isnull=False,
            )
            .distinct()
            .values(
                "code",
                "name",
                "organization__date_created",
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

        communes_with_org = {
            f"{commune['code']}-{commune['name']}": {
                "date": commune["organization__date_created"],
                "age": get_age(commune["organization__date_created"]),
            }
            for commune in communes
        }
        context["communes_with_org"] = json.dumps(
            communes_with_org, cls=DjangoJSONEncoder
        )
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
