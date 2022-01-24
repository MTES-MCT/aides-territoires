import requests
import datetime
from datetime import timedelta

from django.conf import settings
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum
from django.views.generic.edit import FormMixin

from aids.models import Aid, AidProject
from accounts.models import User
from backers.models import Backer
from stats.models import AidViewEvent, Event, AidSearchEvent, AidContactClickEvent
from organizations.models import Organization
from projects.models import Project
from search.models import SearchPage
from alerts.models import Alert

from stats.forms import StatSearchForm
from accounts.mixins import SuperUserRequiredMixin


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


class DashboardView(SuperUserRequiredMixin, FormMixin, TemplateView):
    template_name = 'stats/dashboard.html'
    form_class = StatSearchForm

    def get_period(self):

        period = timezone.now().strftime('%Y-%m-%d')

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                if form.cleaned_data['end_date']:
                    end_date = form.cleaned_data['end_date']
                else:
                    end_date = start_date

                start_date = start_date.strftime('%Y-%m-%d')
                end_date = end_date.strftime('%Y-%m-%d')
                period = start_date.split() + end_date.split()

        return period

    def get_matomo_stats(self, method, start_date, end_date):
        '''
        Here we want to get the stats from Matomo.
        '''

        url = "https://stats.data.gouv.fr/"

        params = {
            'idSite': settings.MATOMO_SITE_ID,
            'module': 'API',
            'method': method,
            'period': 'range',
            'date': f'{start_date},{end_date}',
            'format': 'json',
        }
        res = requests.get(url, params=params)
        data = res.json()
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET:
            form = StatSearchForm(self.request.GET)
            if form.is_valid():
                if form.errors:
                    if form.errors['start_date']:
                        context['start_date_error'] = form.errors['start_date']

        period = self.get_period()
        print(period)
        if type(period) is not str:
            start_date = period[0]
            end_date = period[1]
            end_date_range = datetime.datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        else:
            start_date = period
            end_date = start_date
            end_date_range = datetime.datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

        aids_live_qs = Aid.objects.live()
        matomo_visits_summary = self.get_matomo_stats('VisitsSummary.get', start_date, end_date)
        matomo_actions = self.get_matomo_stats('Actions.get', start_date, end_date)
        matomo_referrers = self.get_matomo_stats('Referrers.get', start_date, end_date)

        # general stats:
        context['nb_beneficiary_accounts'] = User.objects.filter(is_beneficiary=True).count()
        context['nb_organizations'] = Organization.objects.count()
        context['nb_projects'] = Project.objects.count()
        context['nb_aids_live'] = aids_live_qs.count()
        context['nb_aids_matching_projects'] = aids_live_qs \
            .exclude(projects=None) \
            .distinct() \
            .count()
        context['nb_active_financers'] = Backer.objects.has_financed_aids().count()
        context['nb_searchPage'] = SearchPage.objects.count()

        # stats 'Collectivités':
        context['nb_communes'] = Organization.objects \
            .filter(organization_type__contains=['commune']) \
            .count()
        context['nb_epci'] = Organization.objects \
            .filter(organization_type__contains=['epci']) \
            .count()
        context['nb_departments'] = Organization.objects \
            .filter(organization_type__contains=['department']) \
            .count()
        context['nb_regions'] = Organization.objects \
            .filter(organization_type__contains=['region']) \
            .count()

        # stats 'Consultation':
        context['nb_viewed_aids'] = AidViewEvent.objects \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()
        # la valeur "nb_uniq_visitors" n'est pas renvoyée quand period=range
        if 'nb_uniq_visitors' in matomo_visits_summary:
            context['nb_uniq_visitors'] = matomo_visits_summary['nb_uniq_visitors']
        context['nb_visits'] = matomo_visits_summary['nb_visits']
        context['bounce_rate'] = matomo_visits_summary['bounce_rate']
        context['avg_time_on_site'] = matomo_visits_summary['avg_time_on_site']
        context['nb_pageviews'] = matomo_actions['nb_pageviews']

        # stats 'Acquisition':
        context['nb_direct_visitors'] = matomo_referrers['Referrers_visitorsFromDirectEntry']
        context['nb_searchEngine_visitors'] = matomo_referrers['Referrers_visitorsFromSearchEngines'] # noqa
        context['nb_webSite_visitors'] = matomo_referrers['Referrers_visitorsFromWebsites']
        context['nb_newsletter_visitors'] = matomo_referrers['Referrers_visitorsFromCampaigns']
        context['nb_socialNetwork_visitors'] = matomo_referrers['Referrers_visitorsFromSocialNetworks'] # noqa

        # stats 'Engagement':
        context['nb_search_events'] = AidSearchEvent.objects \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()
        context['nb_alerts_created'] = Alert.objects \
            .filter(validated=True) \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()
        context['nb_aid_contact_click_events'] = AidContactClickEvent.objects \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()

        # stats for beneficiaries:
        context['nb_beneficiary_accounts_created'] = User.objects \
            .filter(is_beneficiary=True) \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()
        context['nb_beneficiary_organizations'] = Organization.objects \
            .filter(beneficiaries__is_beneficiary=True) \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()
        context['nb_projects_for_period'] = Project.objects \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()
        context['nb_aids_matching_projects_for_period'] = AidProject.objects \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()

        # stats for contributors:
        context['nb_contributor_accounts_created'] = User.objects \
            .filter(is_contributor=True) \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()
        context['nb_contributor_organizations'] = Organization.objects \
            .filter(beneficiaries__is_contributor=True) \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()
        context['nb_aids_live_for_period'] = aids_live_qs \
            .filter(date_created__range=[start_date, end_date_range]) \
            .count()

        return context
