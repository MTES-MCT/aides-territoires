import requests
import json
from datetime import timedelta

from django.conf import settings
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


    def get_matomo_stats(self, method):
        '''
        Here we want to get the stats from Matomo.
        '''

        url = "https://stats.data.gouv.fr/"

        params = {
            'idSite': settings.MATOMO_SITE_ID,
            'module': 'API',
            'method': method,
            'period': 'day',
            'date': 'today',
            'format': 'json',
        }
        res = requests.get(url, params=params)
        data = res.json()
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        one_week_ago = timezone.now() - timedelta(days=7)
        aids_live_qs = Aid.objects.live()
        matomo_visits_summary = self.get_matomo_stats('VisitsSummary.get')
        matomo_actions = self.get_matomo_stats('Actions.get')
        matomo_referrers = self.get_matomo_stats('Referrers.get')

        # general stats: 
        context['nb_beneficiary_accounts'] = User.objects.filter(is_beneficiary=True).count()
        context['nb_organizations'] = Organization.objects.count()
        context['nb_projects'] = Project.objects.count()
        context['nb_aids_live'] = aids_live_qs.count()
        context['nb_aids_matching_projects'] = aids_live_qs.exclude(projects=None).distinct().count()
        context['nb_active_financers'] = Backer.objects.has_financed_aids().count()
        context['nb_searchPage'] = SearchPage.objects.count()

        # stats 'Collectivités':
        context['nb_communes'] = Organization.objects.filter(organization_type__contains=['commune']).count()
        context['nb_epci'] = Organization.objects.filter(organization_type__contains=['epci']).count()
        context['nb_departments'] = Organization.objects.filter(organization_type__contains=['department']).count()
        context['nb_regions'] = Organization.objects.filter(organization_type__contains=['region']).count()

        # stats 'Consultation':
        context['nb_viewed_aids'] = AidViewEvent.objects.count()
        # Bon à savoir : la valeur "nb_uniq_visitors" n'est pas renvoyé quand on fait period=range
        context['nb_uniq_visitors'] = matomo_visits_summary['nb_uniq_visitors']
        context['nb_visits'] = matomo_visits_summary['nb_visits']
        context['bounce_rate'] = matomo_visits_summary['bounce_rate']
        context['avg_time_on_site'] = matomo_visits_summary['avg_time_on_site']
        context['nb_pageviews'] = matomo_actions['nb_pageviews']

        # stats 'Acquisition':
        context['nb_direct_visitors'] = matomo_referrers['Referrers_visitorsFromDirectEntry']
        context['nb_searchEngine_visitors'] = matomo_referrers['Referrers_visitorsFromSearchEngines']
        context['nb_webSite_visitors'] = matomo_referrers['Referrers_visitorsFromWebsites']
        context['nb_newsletter_visitors'] = matomo_referrers['Referrers_visitorsFromCampaigns']
        context['nb_socialNetwork_visitors'] = matomo_referrers['Referrers_visitorsFromSocialNetworks']

        # stats 'Engagement':
        context['nb_search_events'] = AidSearchEvent.objects.count()
        context['nb_alerts_created'] = Alert.objects.filter(validated=True).count()
        context['nb_aid_contact_click_events'] = AidContactClickEvent.objects.count()
        
        # stats for beneficiaries:
        context['nb_beneficiary_accounts_created'] = User.objects.filter(is_beneficiary=True).count()
        context['nb_beneficiary_organizations'] = Organization.objects.filter(beneficiaries__is_beneficiary=True).count()
        context['nb_projects_for_period'] = Project.objects.count()
        context['nb_aids_matching_projects_for_period'] = aids_live_qs.exclude(projects=None).distinct().count()

        # stats for contributors:
        context['nb_contributor_accounts_created'] = User.objects.filter(is_contributor=True).count()
        context['nb_contributor_organizations'] = Organization.objects.filter(beneficiaries__is_contributor=True).count()
        context['nb_aids_live_for_period'] = Aid.objects.live().count()

        return context
