from datetime import timedelta

from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum, Q, Count, F, Func, Value, CharField

from aids.models import Aid
from alerts.models import Alert
from backers.models import Backer
from stats.models import Event


class StatsView(TemplateView):
    template_name = 'stats/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        aids_qs = Aid.objects.live()
        context['nb_live_aids'] = aids_qs.count()

        one_week_ago = timezone.now() - timedelta(days=8)
        viewed_aids_qs = Event.objects.filter(category='aid', event='viewed') \
            .filter(date_created__gte=one_week_ago)
        context['nb_viewed_aids_1_week'] = viewed_aids_qs.count()

        viewed_aids_timeseries = Event.objects \
            .filter(category='aid', event='viewed') \
            .annotate(day=Func(
                F('date_created'),
                Value('YYYY-MM-01'),
                function='to_char',
                output_field=CharField())) \
            .values('day') \
            .annotate(y=Count('id')) \
            .order_by()
        context['nb_viewed_aids_timeseries'] = list(viewed_aids_timeseries)

        alerts_qs = Event.objects \
            .filter(category='alert', event='sent') \
            .aggregate(nb_sent_alerts=Sum('value'))
        context['nb_sent_alerts'] = alerts_qs['nb_sent_alerts']

        alerts_created_timeseries = Alert.objects.filter(validated=True) \
            .annotate(day=Func(
                F('date_created'),
                Value('YYYY-MM-01'),
                function='to_char',
                output_field=CharField())) \
            .values('day') \
            .annotate(y=Count('token')) \
            .order_by()
        context['nb_alerts_created_timeseries'] = list(alerts_created_timeseries)  # noqa

        financers = aids_qs.values_list('financers', flat=True)
        instructors = aids_qs.values_list('instructors', flat=True)
        nb_backers = Backer.objects \
            .filter(Q(id__in=financers) | Q(id__in=instructors)) \
            .values('id') \
            .count()
        context['nb_backers'] = nb_backers

        return context
