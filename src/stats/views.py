from datetime import timedelta

from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum

from aids.models import Aid
from accounts.models import User
from backers.models import Backer
from stats.models import AidViewEvent, Event, AidSearchEvent, AidContactClickEvent
from organizations.models import Organization
from projects.models import Project
from search.models import SearchPage
from alerts.models import Alert


class StatsView(TemplateView):
    template_name = 'stats/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        aids_qs = Aid.objects.live()
        context['nb_live_aids'] = aids_qs.count()

        one_week_ago = timezone.now() - timedelta(days=7)
        viewed_aids_qs = AidViewEvent.objects \
            .filter(date_created__gte=one_week_ago)
        context['nb_viewed_aids'] = viewed_aids_qs.count()

        alerts_qs = Event.objects \
            .filter(category='alert', event='sent') \
            .aggregate(nb_sent_alerts=Sum('value'))
        context['nb_sent_alerts'] = alerts_qs['nb_sent_alerts']

        active_backers = Backer.objects.has_financed_aids()
        context['nb_backers'] = active_backers.count()

        return context


class DashboardView(TemplateView):
    template_name = 'stats/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        one_week_ago = timezone.now() - timedelta(days=7)
        aids_live_qs = Aid.objects.live()

        context['nb_beneficiary_accounts'] = User.objects.filter(is_beneficiary=True).count()
        context['nb_organizations'] = Organization.objects.count()
        context['nb_projects'] = Project.objects.count()
        context['nb_aids_live'] = aids_live_qs.count()
        context['nb_aids_matching_projects'] = aids_live_qs.exclude(projects=None).distinct().count()
        context['nb_active_financers'] = Backer.objects.has_financed_aids().count()
        context['nb_searchPage'] = SearchPage.objects.count()
        context['nb_viewed_aids'] = AidViewEvent.objects.count()
        context['nb_alerts_created'] = Alert.objects.filter(validated=True).count()
        context['nb_search_events'] = AidSearchEvent.objects.count()
        context['nb_aid_contact_click_events'] = AidContactClickEvent.objects.count()
        return context
