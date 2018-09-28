from datetime import timedelta

from django.views.generic import TemplateView
from django.utils import timezone

from aids.models import Aid


class StatsView(TemplateView):
    template_name = 'stats/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        aids_qs = Aid.objects.published()
        context['nb_all_aids'] = aids_qs.count()
        context['nb_active_aids'] = aids_qs.open().count()

        one_month_ago = timezone.now() - timedelta(days=31)
        recently_updated_qs = aids_qs \
            .open() \
            .filter(date_updated__gte=one_month_ago)
        context['nb_updated_aids'] = recently_updated_qs.count()

        authors_qs = aids_qs \
            .open() \
            .values('author') \
            .distinct()
        context['nb_active_users'] = authors_qs.count()

        return context
