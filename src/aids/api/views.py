from rest_framework import viewsets

from aids.models import Aid
from aids.api.serializers import AidSerializer
from aids.forms import AidSearchForm


class AidViewSet(viewsets.ReadOnlyModelViewSet):
    """List all active aids that we know about."""

    serializer_class = AidSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Aid.objects \
            .published() \
            .open() \
            .select_related('perimeter') \
            .prefetch_related('financers', 'instructors') \
            .order_by('perimeter__scale', 'submission_deadline')

        filter_form = AidSearchForm(data=self.request.GET)
        filtered_qs = filter_form.filter_queryset(qs)
        return filtered_qs
