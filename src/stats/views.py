from datetime import timedelta

from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum

from aids.models import Aid
from stats.models import Event


class StatsView(TemplateView):
    template_name = 'stats/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        aids_qs = Aid.objects.published().open()
        context['nb_active_aids'] = aids_qs.count()

        one_week_ago = timezone.now() - timedelta(days=8)
        viewed_aids_qs = Event.objects.filter(category='aid', event='viewed') \
            .filter(date_created__gte=one_week_ago)
        context['nb_viewed_aids'] = viewed_aids_qs.count()

        alerts_qs = Event.objects \
            .filter(category='alert', event='sent') \
            .aggregate(nb_sent_alerts=Sum('value'))
        context['nb_sent_alerts'] = alerts_qs['nb_sent_alerts']

        # financers = aids_qs.values
        financers = aids_qs.values_list('financers', flat=True)
        instructors = aids_qs.values_list('instructors', flat=True)
        nb_backers = len(set(list(financers) + list(instructors)))
        context['nb_backers'] = nb_backers

        return context
