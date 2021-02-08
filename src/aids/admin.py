from functools import reduce
from operator import and_

from django.db.models import Q, CharField, Value as V
from django.db.models.functions import Concat
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.safestring import mark_safe

from import_export.admin import ExportActionMixin
from import_export.formats import base_formats
from admin_auto_filters.filters import AutocompleteFilter

from aids.utils import generate_clone_title
from aids.admin_views import AmendmentMerge
from aids.forms import AidAdminForm
from aids.models import Aid, AidWorkflow
from aids.resources import AidResource
from core.admin import InputFilter
from exporting.tasks import export_aids_as_csv, export_aids_as_xlsx
from geofr.utils import get_all_related_perimeter_ids
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class LiveAidListFilter(admin.SimpleListFilter):
    """Custom admin filter to target aids with various statuses."""

    title = _('State')
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return (
            # aid.state
            ('open', _('Open aids')),
            ('deadline', _('Deadline approaching aids')),
            ('expired', _('Expired aids')),
            # aid.display_status
            ('hidden', _('Currently not displayed')),
            ('live', _('Currently displayed')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'open':
            return queryset.open()

        if self.value() == 'expired':
            return queryset.expired()

        if self.value() == 'deadline':
            return queryset.soon_expiring()

        if self.value() == 'hidden':
            return queryset.hidden()

        if self.value() == 'live':
            return queryset.published().open()


class AuthorFilter(InputFilter):
    parameter_name = 'author'
    title = _('Author')

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            qs = queryset \
                .annotate(
                    author_name=Concat(
                        'author__first_name', V(' '), 'author__last_name',
                        output_field=CharField())) \
                .filter(Q(author_name__icontains=value))
            return qs


class BackersFilter(InputFilter):
    parameter_name = 'backers'
    title = _('Backers')

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            bits = value.split(' ')
            financer_filters = [
                Q(financers__name__icontains=bit)
                for bit in bits
            ]
            instructor_filters = [
                Q(instructors__name__icontains=bit)
                for bit in bits
            ]
            return queryset.filter(
                Q(reduce(and_, financer_filters)) |
                Q(reduce(and_, instructor_filters)))


class PerimeterFilter(InputFilter):
    parameter_name = 'perimeter'
    title = _('Perimeter')

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            return queryset.filter(Q(perimeter__name__icontains=value))


class PerimeterAutocompleteFilter(AutocompleteFilter):
    field_name = 'perimeter'
    title = _('Perimeter')
    use_pk_exact = False

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            perimeter_qs = get_all_related_perimeter_ids(value)
            return queryset.filter(perimeter__in=perimeter_qs)


class BaseAidAdmin(ExportActionMixin, admin.ModelAdmin):
    """Admin module for aids."""

    class Media:
        css = {
            'all': (
                '/static/css/admin.css',
                '/static/trumbowyg/dist/ui/trumbowyg.css',
            )
        }
        js = [
            'admin/js/jquery.init.js',
            '/static/js/shared_config.js',
            '/static/js/plugins/softmaxlength.js',
            '/static/js/aids/enable_softmaxlength.js',
            '/static/trumbowyg/dist/trumbowyg.js',
            '/static/trumbowyg/dist/langs/fr.js',
            '/static/js/enable_rich_text_editor.js',
            '/static/js/aids/duplicate_buster.js',
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS

    form = AidAdminForm
    resource_class = AidResource
    ordering = ['-id']
    save_as = True
    actions = [
        'export_csv', 'export_xlsx', 'export_admin_action',
        'make_mark_as_CFP']
    formats = [base_formats.CSV, base_formats.XLSX]
    list_display = [
        'live_status', 'name', 'all_financers', 'all_instructors',
        'author_name', 'recurrence', 'date_updated', 'date_published',
        'is_imported', 'submission_deadline', 'status', 'aid_typology',
    ]
    list_display_links = ['name']
    autocomplete_fields = ['author', 'financers', 'instructors', 'perimeter',
                           'programs']
    search_fields = ['name']
    list_filter = [
        'status', 'aid_typology', 'recurrence', 'is_imported',
        'is_call_for_project', 'in_france_relance',
        LiveAidListFilter, AuthorFilter, BackersFilter,
        PerimeterAutocompleteFilter,
        'programs', 'categories']

    filter_vertical = ['categories']  # Overriden in the widget definition
    readonly_fields = [
        'is_imported', 'import_uniqueid', 'import_data_url',
        'import_share_licence', 'import_last_access', 'date_created',
        'date_updated', 'date_published']
    raw_id_fields = ['generic_aid']
    fieldsets = [
        (_('Aid presentation'), {
            'fields': (
                'name',
                'slug',
                'in_france_relance',
                'short_title',
                'categories',
                'targeted_audiences',
                'financers',
                'financer_suggestion',
                'instructors',
                'instructor_suggestion',
                'author',
            )
        }),

        (_('Aid perimeter'), {
            'fields': (
                'perimeter',
                'perimeter_suggestion',
            )
        }),

        (_('Aid calendar'), {
            'fields': (
                'recurrence',
                'start_date',
                'predeposit_date',
                'submission_deadline',
            )
        }),

        (_('Aid typology'), {
            'fields': (
                'aid_typology',
                'generic_aid',
                'local_characteristics',
            )
        }),

        (_('Aid description'), {
            'fields': (
                'is_call_for_project',
                'programs',
                'aid_types',
                'subvention_rate',
                'subvention_comment',
                'mobilization_steps',
                'destinations',
                'description',
                'project_examples',
                'eligibility',
            )
        }),

        (_('Contact and actions'), {
            'fields': (
                'origin_url',
                'application_url',
                'contact',
            )
        }),

        (_('Aid admin'), {
            'fields': (
                'status',
            )
        }),

        (_('Import related data'), {
            'fields': (
                'is_imported',
                'import_uniqueid',
                'import_data_url',
                'import_share_licence',
                'import_last_access',
            )
        }),
        (_('Misc data'), {
            'fields': (
                'date_created',
                'date_updated',
                'date_published',
            )
        }),
    ]

    def author_name(self, aid):
        return aid.author.full_name
    author_name.short_description = _('Author')

    def all_financers(self, aid):
        financers = [backer.name for backer in aid.financers.all()]
        return ', '.join(financers)
    all_financers.short_description = _('Financers')

    def all_instructors(self, aid):
        instructors = [backer.name for backer in aid.instructors.all()]
        return ', '.join(instructors)
    all_instructors.short_description = _('Instructors')

    def live_status(self, aid):
        return aid.is_live()
    live_status.boolean = True
    live_status.short_description = _('Live')

    def make_mark_as_CFP(self, request, queryset):
        queryset.update(is_call_for_project=True)
        self.message_user(request, _('The selected aids were set as CFP'))
    make_mark_as_CFP.short_description = _('Set as CFP')

    def show_export_message(self, request):
        url = reverse('admin:exporting_dataexport_changelist')
        msg = _(
            f'Exported data will be available '
            f'<a href="{url}">here: {url}</a>')
        self.message_user(request, mark_safe(msg))

    def export_csv(self, request, queryset):
        aids_id_list = list(queryset.values_list('id', flat=True))
        export_aids_as_csv.delay(aids_id_list, request.user.id)
        self.show_export_message(request)
    export_csv.short_description = _(
        'Export selected Aids as CSV in background task')

    def export_xlsx(self, request, queryset):
        aids_id_list = list(queryset.values_list('id', flat=True))
        export_aids_as_xlsx.delay(aids_id_list, request.user.id)
        self.show_export_message(request)
    export_xlsx.short_description = _(
        'Export selected Aids as XLSX as background task')

    def export_admin_action(self, request, queryset):
        # We do a noop override of this method, just because
        # we want to customize it's short description
        return super().export_admin_action(request, queryset)
    export_admin_action.short_description = _(
        'Export and download selected Aids')


class AidAdmin(BaseAidAdmin):
    def get_queryset(self, request):
        qs = Aid.objects \
            .all() \
            .distinct() \
            .prefetch_related('financers', 'instructors') \
            .select_related('author')
        return qs

    def delete_model(self, request, obj):
        obj.soft_delete()

    def delete_queryset(self, request, queryset):
        queryset.update(status='deleted')

    def save_model(self, request, obj, form, change):
        # When cloning an existing aid, prefix it's title with "[Copie]"
        if '_saveasnew' in request.POST:
            obj.name = generate_clone_title(obj.name)
            obj.status = AidWorkflow.states.draft
        return super().save_model(request, obj, form, change)


class DeletedAid(Aid):
    class Meta:
        proxy = True
        verbose_name = _('Deleted aid')
        verbose_name_plural = _('Deleted aids')


class DeletedAidAdmin(BaseAidAdmin):
    def get_queryset(self, request):
        qs = Aid.deleted_aids \
            .all() \
            .prefetch_related('financers', 'instructors') \
            .select_related('author')
        return qs


class Amendment(Aid):
    """We need this so we can register the same model twice."""
    class Meta:
        proxy = True
        verbose_name = _('Amendment')
        verbose_name_plural = _('Amendments')


class AmendmentChangeList(ChangeList):
    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        url = reverse('admin:aids_amendment_merge', args=[pk])
        return url


class AmendmentAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'amended_aid', 'amendment_author_name', 'date_created'
    ]

    def get_queryset(self, request):
        qs = Aid.amendments.all()
        qs = qs.prefetch_related('financers')
        qs = qs.select_related('author')
        return qs

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(_('<path:object_id>/merge/'), self.admin_site.admin_view(
                AmendmentMerge.as_view()), name='aids_amendment_merge'),
        ]
        return my_urls + urls

    def get_changelist(self, request, **kwargs):
        return AmendmentChangeList


admin.site.register(Aid, AidAdmin)
admin.site.register(DeletedAid, DeletedAidAdmin)
admin.site.register(Amendment, AmendmentAdmin)
