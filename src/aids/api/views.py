from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from django.conf import settings

from aids.models import Aid
from aids.api.serializers import AidSerializer
from aids.forms import AidSearchForm


class AidViewSet(viewsets.ReadOnlyModelViewSet):
    """List all active aids that we know about."""

    lookup_field = 'slug'

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Aid.objects \
            .published() \
            .open() \
            .select_related('perimeter') \
            .prefetch_related('financers', 'instructors') \
            .order_by('perimeter__scale', 'submission_deadline')

        filter_form = AidSearchForm(data=self.request.GET)
        results = filter_form.filter_queryset(qs)
        ordered_results = filter_form.order_queryset(results).distinct()
        return ordered_results

    def get_serializer_class(self):
        version = self.request.version
        if version == settings.CURRENT_API_VERSION or version is None:
            serializer_class = AidSerializer
        else:
            raise NotFound('This api version does not exist.')

        return serializer_class
