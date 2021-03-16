from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework.exceptions import NotFound


from aids.models import Aid
from aids.api.serializers import (
    AidSerializer10, AidSerializer11, AidSerializer12, AidSerializerLatest)
from aids.forms import AidSearchForm
from stats.utils import log_aidviewevent, log_aidsearchevent


def noop_decorator(func):
    return func


cache_list_page = noop_decorator
if settings.ENABLE_AID_LIST_API_CACHE:
    timeout = settings.AID_LIST_API_CACHE_TIMEOUT
    cache_list_page = method_decorator(cache_page(timeout))

cache_detail_page = noop_decorator
if settings.ENABLE_AID_DETAIL_API_CACHE:
    timeout = settings.AID_DETAIL_API_CACHE_TIMEOUT
    cache_detail_page = method_decorator(cache_page(timeout))


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

    @cache_list_page
    def list(self, request):
        return super().list(request)

    @cache_detail_page
    def retrieve(self, request, slug):
        return super().retrieve(request, slug)

    def finalize_response(self, request, response, *args, **kwargs):
        # Fetching only 1 aid --> AidViewEvent
        if self.detail:
            if response.data.get('id'):
                log_aidviewevent.delay(
                    aid_id=response.data.get('id'),
                    querystring=self.request.GET.urlencode(),
                    source='api')
        # Fetching all aids (with or without filters) --> AidSearchEvent
        else:
            log_aidsearchevent.delay(
                querystring=self.request.GET.urlencode(),
                results_count=response.data.get('count', 0),
                source='api')
        return super().finalize_response(request, response, *args, **kwargs)
