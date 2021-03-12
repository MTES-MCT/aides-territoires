from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from django.conf import settings

from aids.models import Aid
from aids.api.serializers import (
    AidSerializer10, AidSerializer11, AidSerializer12, AidSerializerLatest)
from aids.forms import AidSearchForm
from stats.utils import log_aidsearchevent


class AidViewSet(viewsets.ReadOnlyModelViewSet):
    """List all active aids that we know about."""

    lookup_field = 'slug'

    def get_base_queryset(self):
        """Get the base queryset of aid list.

        For some backend features, we must allow superusers to search among
        all aids (including aids that are not live on the frontend).
        """

        qs = Aid.objects \
            .select_related('perimeter') \
            .prefetch_related(
                'financers', 'instructors', 'programs', 'categories__theme') \
            .order_by('perimeter__scale', 'submission_deadline')

        if self.request.user.is_superuser and 'drafts' in self.request.GET:
            # Superusers can search among unfiltered aids
            # (including aid drafts)
            pass
        else:
            # Normal users can only see aids that are actually published
            qs = qs.live()

        return qs

    def get_queryset(self):
        """Filter data according to search query."""

        qs = self.get_base_queryset()
        filter_form = AidSearchForm(data=self.request.GET)
        results = filter_form.filter_queryset(qs)
        ordered_results = filter_form.order_queryset(results).distinct()
        return ordered_results

    def get_serializer_class(self):
        version = self.request.version

        if version == settings.CURRENT_API_VERSION or version is None:
            serializer_class = AidSerializerLatest
        elif version == '1.2':
            serializer_class = AidSerializer12
        elif version == '1.1':
            serializer_class = AidSerializer11
        elif version == '1.0':
            serializer_class = AidSerializer10
        else:
            raise NotFound('This api version does not exist.')

        return serializer_class

    def finalize_response(self, request, response, *args, **kwargs):
        if self.detail:
            results_count = 1
        else:
            results_count = response.data.get('count', 0)
        log_aidsearchevent.delay(
            querystring=self.request.GET.urlencode(),
            results_count=results_count,
            source='api')
        return super().finalize_response(request, response, *args, **kwargs)
