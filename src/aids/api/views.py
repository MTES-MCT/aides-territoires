from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from core.api.pagination import ApiPagination
from aids.models import Aid
from aids.constants import AUDIENCES_GROUPED, TYPES_GROUPED
from aids.api import doc as api_doc
from aids.api.serializers import (
    AidSerializer10, AidSerializer11, AidSerializer12, AidSerializerLatest,
    AidAudienceSerializer, AidTypeSerializer, AidStepSerializer, AidRecurrenceSerializer, AidDestinationSerializer)  # noqa
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


class AidViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'
    pagination_class = ApiPagination

    def get_base_queryset(self):
        """Get the base queryset of aid list.

        For some backend features, we must allow superusers to search among
        all aids (including aids that are not live on the frontend).
        """

        qs = Aid.objects \
            .select_related('perimeter') \
            .prefetch_related('financers', 'instructors', 'programs', 'categories__theme') \
            .order_by('perimeter__scale', 'submission_deadline')

        if self.request.user.is_superuser and 'drafts' in self.request.GET:
            # Superusers can search among unfiltered aids (including aid drafts)
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
        version = getattr(self.request, 'version', None)

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

    @extend_schema(
        summary="Lister toutes les aides actuellement publiées",
        parameters=api_doc.aids_api_parameters,
        tags=[Aid._meta.verbose_name_plural])
    @cache_list_page
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(
        summary="Afficher l'aide donnée",
        tags=[Aid._meta.verbose_name_plural])
    @cache_detail_page
    def retrieve(self, request, slug=None, *args, **kwargs):
        return super().retrieve(request, slug, args, kwargs)

    @extend_schema(
        summary="Toutes les aides au format JSON",
        description="La donnée retournée n'est pas temps-réel, \
        le résultat est mis à jour à interval régulier."
        "<br /><br />"
        "Si votre application requiert de la donnée temps-réel, alors cette ressource n'est pas \
        adaptée. Tournez-vous vers `/api/aids/`.",
        tags=[Aid._meta.verbose_name_plural])
    @action(detail=False)
    def all(self, request):
        file_url = storage.url(settings.ALL_AIDS_DUMP_FILE_PATH)
        return redirect(file_url)

    def get_aids_count(self, response):
        """
        The number of aids can be found in the response data : that's the case
        when the API uses pagination.
        Sometime, we cannot get this count from the response data : that's the
        case when the user is requesting a dump of all aids. In that case, we
        just use the current aids count from the DB, even though that count
        could be outdated, because the results are not fetched in real-time.
        """
        if hasattr(response, 'data') and 'count' in response.data:
            count = response.data.get('count', 0)
        else:
            count = self.get_queryset().count()
        return count

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
                results_count=self.get_aids_count(response),
                source='api',
                request_ua=request_ua)

        return super().finalize_response(request, response, *args, **kwargs)


class AidAudiencesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AidAudienceSerializer

    def get_queryset(self):
        aid_audiences = list()
        for (audience_type, audience_group) in AUDIENCES_GROUPED:
            aid_audiences += [{'id': id, 'name': name, 'type': audience_type} for (id, name) in audience_group]  # noqa
        return aid_audiences

    @extend_schema(
        summary="Lister tous les choix de bénéficiaires",
        tags=[Aid._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class AidTypesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AidTypeSerializer

    def get_queryset(self):
        aid_types = list()
        for (type_type, type_group) in TYPES_GROUPED:
            aid_types += [{'id': id, 'name': name, 'type': type_type} for (id, name) in type_group]  # noqa
        return aid_types

    @extend_schema(
        summary="Lister tous les choix de types d'aides",
        tags=[Aid._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class AidStepsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AidStepSerializer

    def get_queryset(self):
        aid_steps = [{'id': id, 'name': name} for (id, name) in Aid.STEPS]
        return aid_steps

    @extend_schema(
        summary="Lister tous les choix d'états d'avancement",
        tags=[Aid._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class AidRecurrencesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AidRecurrenceSerializer

    def get_queryset(self):
        aid_recurrences = [{'id': id, 'name': name} for (id, name) in Aid.RECURRENCES]
        return aid_recurrences

    @extend_schema(
        summary="Lister tous les choix de récurrences",
        tags=[Aid._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class AidDestinationsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AidDestinationSerializer

    def get_queryset(self):
        aid_destinations = [{'id': id, 'name': name} for (id, name) in Aid.DESTINATIONS]
        return aid_destinations

    @extend_schema(
        summary="Lister tous les choix de types de dépenses",
        tags=[Aid._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
