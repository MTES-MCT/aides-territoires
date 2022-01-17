from datetime import timedelta

from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum

from aids.models import Aid
from accounts.models import User
from backers.models import Backer
from stats.models import AidViewEvent, Event


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

        context['nb_beneficiary_accounts'] = User.objects.filter(is_beneficiary=True).count()

        aids_qs = Aid.objects.live()
        context['nb_live_aids'] = aids_qs.count()

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
