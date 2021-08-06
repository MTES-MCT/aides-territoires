from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from aids.models import Aid
from aids.constants import AUDIENCES_GROUPED, TYPES_GROUPED
from aids.api.serializers import (
    AidSerializer10, AidSerializer11, AidSerializer12, AidSerializerLatest)
from aids.api.pagination import AidsPagination
from aids.forms import AidSearchForm
from stats.utils import log_aidviewevent, log_aidsearchevent


def noop_decorator(func):
    """
    We use this "noop" decorator in order to disable caching.
    """
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
    """List all active aids that we know about.

    Parameters

    - 'prevent_generic_filter': This is used as a flag, for instance :
    '?prevent_generic_filter=yes'. Note that the value here does not
    matter, since we only check whether the parameter is present or not.
    Preventing generic aids filtering means that generic and local variants
    will all be listed. So there will be duplicate aids in results.
    """

    lookup_field = 'slug'
    pagination_class = AidsPagination

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
        apply_filter = 'prevent_generic_filter' not in self.request.GET
        results = filter_form.filter_queryset(qs, apply_generic_aid_filter=apply_filter)
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
        request_ua = request.META.get('HTTP_USER_AGENT', '')
        request_referer = request.META.get('HTTP_REFERER', '')

        # Fetching only 1 aid --> AidViewEvent
        if self.detail:
            if response.data.get('id'):
                log_aidviewevent.delay(
                    aid_id=response.data.get('id'),
                    querystring=request.GET.urlencode(),
                    source='api',
                    request_ua=request_ua,
                    request_referer=request_referer)
        # Fetching all aids (with or without filters) --> AidSearchEvent

        else:
            log_aidsearchevent.delay(
                querystring=request.GET.urlencode(),
                results_count=response.data.get('count', 0),
                source='api',
                request_ua=request_ua)

        return super().finalize_response(request, response, *args, **kwargs)


class AidAudiences(viewsets.ViewSet):
    """
    List all the audiences.
    Exemple : { "key": "commune", "value": "Communes", "type": "Collectivités" }
    """

    def list(self, request):
        aid_audiences = list()
        for (audience_type, audience_group) in AUDIENCES_GROUPED:
            aid_audiences += [{'key': key, 'value': value, 'type': audience_type} for (key, value) in audience_group]  # noqa
        data = {
            'count': len(aid_audiences),
            'results': aid_audiences
        }
        return Response(data)


class AidTypes(viewsets.ViewSet):
    """
    List all the aid types.
    Exemple : { "key": "grant", "value": "Subvention", "type": "Aides financières" }
    """

    def list(self, request):
        aid_types = list()
        for (type_type, type_group) in TYPES_GROUPED:
            aid_types += [{'key': key, 'value': value, 'type': type_type} for (key, value) in type_group]  # noqa
        data = {
            'count': len(aid_types),
            'results': aid_types
        }
        return Response(data)


class AidSteps(viewsets.ViewSet):
    """
    List all the aid steps.
    Example : { "key": "preop", "value": "Réflexion / conception" }
    """

    def list(self, request):
        aid_steps = [{'key': key, 'value': value} for (key, value) in Aid.STEPS]
        data = {
            'count': len(aid_steps),
            'results': aid_steps
        }
        return Response(data)


class AidRecurrences(viewsets.ViewSet):
    """
    List all the aid recurrences.
    Example : { "key": "oneoff", "value": "Ponctuelle" }
    """

    def list(self, request):
        aid_recurrences = [{'key': key, 'value': value} for (key, value) in Aid.RECURRENCES]
        data = {
            'count': len(aid_recurrences),
            'results': aid_recurrences
        }
        return Response(data)


class AidDestinations(viewsets.ViewSet):
    """
    List all the aid destinations.
    Example : { "key": "supply", "value": "Dépenses de fonctionnement" }
    """

    def list(self, request):
        aid_destinations = [{'key': key, 'value': value} for (key, value) in Aid.DESTINATIONS]
        data = {
            'count': len(aid_destinations),
            'results': aid_destinations
        }
        return Response(data)
