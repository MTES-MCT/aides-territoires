import re
from functools import reduce
from operator import and_

from django.db.models import Q
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from import_export.admin import ImportMixin, ExportActionMixin
from import_export.formats import base_formats
from admin_auto_filters.filters import AutocompleteFilter
from fieldsets_with_inlines import FieldsetsInlineMixin
from adminsortable2.admin import SortableInlineAdminMixin

from aids.utils import generate_clone_title
from aids.admin_views import AmendmentMerge
from aids.forms import AidAdminForm
from aids.models import Aid, AidWorkflow, AidFinancer, AidInstructor
from aids.resources import AidResource
from core.admin import InputFilter, pretty_print_readonly_jsonfield
from accounts.admin import AuthorFilter
from search.models import SearchPage
from exporting.tasks import export_aids_as_csv, export_aids_as_xlsx
from exporting.utils import get_admin_export_message
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


class EligibilityTestFilter(admin.SimpleListFilter):
    """Custom admin filter to target aids with eligibility tests."""

    title = "Test d'éligibilité"
    parameter_name = 'has_eligibility_test'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.has_eligibility_test()
        elif value == 'No':
            return queryset.filter(eligibility_test__isnull=True)
        return queryset


class ProjectFilter(admin.SimpleListFilter):
    """Custom admin filter to target aids with projects."""

    title = _('Aids associated to projects')
    parameter_name = 'has_projects'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.has_projects()
        elif value == 'No':
            return queryset.filter(projects__isnull=True)  # noqa
        return queryset


class GenericAidListFilter(admin.SimpleListFilter):
    """Custom admin filter for generic, local and standard aids."""

    title = _('Generic / Local')
    parameter_name = 'typology'

    def lookups(self, request, model_admin):
        return (
            ('generic', _('Generic aids')),
            ('local', _('Local aids')),
            ('standard', _('Standard aids')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'generic':
            return queryset.generic_aids()

        if self.value() == 'local':
            return queryset.local_aids()

        if self.value() == 'standard':
            return queryset.standard_aids()


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

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            perimeter_qs = get_all_related_perimeter_ids(value)
            return queryset.filter(perimeter__in=perimeter_qs)


class FinancersInline(SortableInlineAdminMixin, admin.TabularInline):
    """Configure the formset to the financers m2m field."""

    model = AidFinancer
    extra = 1
    verbose_name = "Porteur d'aide"
    verbose_name_plural = "Porteurs d'aides"
    autocomplete_fields = ['backer']


class InstructorsInline(SortableInlineAdminMixin, admin.TabularInline):
    """Configure the formset to the instructors m2m field."""

    model = AidInstructor
    extra = 1
    verbose_name = 'Instructeur'
    verbose_name_plural = 'Instructeurs'
    autocomplete_fields = ['backer']


class BaseAidAdmin(FieldsetsInlineMixin,
                   ImportMixin, ExportActionMixin,
                   admin.ModelAdmin):
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
            '/static/js/project_autocomplete_admin.js',
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
        'author_name', 'recurrence', 'perimeter', 'date_updated',
        'date_published', 'is_imported', 'submission_deadline', 'status']
    list_display_links = ['name']
    search_fields = ['id', 'name']
    list_filter = [
        'status', LiveAidListFilter, GenericAidListFilter, 'recurrence',
        'is_imported', 'import_data_source',
        'is_call_for_project', 'in_france_relance',
        EligibilityTestFilter, ProjectFilter, AuthorFilter, BackersFilter,
        PerimeterAutocompleteFilter,
        'programs', 'categories__theme', 'categories']

    autocomplete_fields = ['author', 'financers', 'instructors', 'perimeter',
                           'programs']
    filter_vertical = [
        'categories',
    ]  # Overriden in the widget definition
    readonly_fields = [
        'sibling_aids',
        'is_imported', 'import_data_source', 'import_uniqueid', 'import_data_url', 'import_share_licence', 'import_last_access',  # noqa
        'get_pprint_import_raw_object',
        'date_created', 'date_updated', 'date_published']
    raw_id_fields = ['generic_aid']

    fieldsets_with_inlines = [
        (_('Aid presentation'), {
            'fields': (
                'name',
                'slug',
                'in_france_relance',
                'short_title',
                'categories',
                'targeted_audiences',
                'financer_suggestion',
                'instructor_suggestion',
                'author',
                'sibling_aids',
            )
        }),

        FinancersInline,
        InstructorsInline,

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

        (_('Aid description'), {
            'fields': (
                'is_call_for_project',
                'programs',
                'aid_types',
                'subvention_rate',
                'subvention_comment',
                'loan_amount',
                'recoverable_advance_amount',
                'other_financial_aid_comment',
                'mobilization_steps',
                'destinations',
                'description',
                'projects',
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

        ('Éligibilité', {
            'fields': (
                'eligibility_test',
            )
        }),

        (_('Aid admin'), {
            'fields': (
                'status',
            )
        }),

        (_('Only for generic aids'), {
            'fields': (
                'is_generic',
            )
        }),

        (_('Only for local aids'), {
            'fields': (
                'generic_aid',
                'local_characteristics',
            )
        }),


        (_('Import related data'), {
            'fields': (
                'is_imported',
                'import_data_source',
                'import_uniqueid',
                'import_data_url',
                'import_share_licence',
                'import_last_access',
                'get_pprint_import_raw_object',
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

    def get_search_results(self, request, queryset, search_term):
        """
        Here we can override the result of 'aids' autocomplete_fields
        used in other admins.
        Usage:
        - autocomplete_fields is used on 'highlighted_aids' in the SearchPage
        admin. But we want to restrict the queryset to only the SearchPage aids
        """

        queryset, use_distinct = super().get_search_results(request, queryset, search_term)  # noqa

        # e.g. '<host>/admin/search/searchpage/35/change/'
        meta_http_referer = request.META.get('HTTP_REFERER', '')
        # e.g. 'app_label=search&model_name=searchpage&field_name=highlighted_aids'  # noqa
        meta_query_string = request.META.get('QUERY_STRING', '')

        # custom SearchPage.highlighted_aids autocomplete filter
        if meta_query_string and all(x in meta_query_string for x in ['searchpage', 'highlighted_aids']):  # noqa
            try:
                search_page_id_str = re.search('searchpage/(.*?)/change', meta_http_referer).group(1)  # noqa
                queryset = SearchPage.objects.get(pk=int(search_page_id_str)) \
                                             .get_base_queryset(all_aids=True)
            except AttributeError:  # regex error
                pass

        return queryset, use_distinct

    def sibling_aids(self, aid):
        """Number of other (non draft) aids created by the same author."""

        return Aid.objects \
            .exclude(id=aid.id) \
            .filter(author=aid.author) \
            .filter(status__in=('reviewable', 'published')) \
            .count()
    sibling_aids.short_description = _('From the same author')
    sibling_aids.help_text = _('Nb of (non-draft) aids by the same author')

    def get_form(self, request, obj=None, **kwargs):
        """Set readonly fields help texts."""
        help_texts = {'sibling_aids': self.sibling_aids.help_text}
        kwargs.update({'help_texts': help_texts})
        return super().get_form(request, obj, **kwargs)

    def author_name(self, aid):
        if aid.author is not None:
            return aid.author.full_name
    author_name.short_description = _('Author')

    def all_financers(self, aid):
        financers = [backer.name for backer in aid.financers.all()]
        return ', '.join(financers)
    all_financers.short_description = "Porteurs d'aides"

    def all_instructors(self, aid):
        instructors = [backer.name for backer in aid.instructors.all()]
        return ', '.join(instructors)
    all_instructors.short_description = 'Instructeurs'

    def live_status(self, aid):
        return aid.is_live()
    live_status.boolean = True
    live_status.short_description = _('Live')

    def has_projects(self, aid):
        return aid.has_projects()
    has_projects.boolean = True
    has_projects.short_description = _('Has projects associated')

    def has_eligibility_test(self, aid):
        return aid.has_eligibility_test()
    has_eligibility_test.boolean = True
    has_eligibility_test.short_description = "Test d'éligibilité"

    def get_pprint_import_raw_object(self, obj=None):
        if obj:
            return pretty_print_readonly_jsonfield(obj.import_raw_object)
        return ''
    get_pprint_import_raw_object.short_description = 'Donnée brute importée'

    def make_mark_as_CFP(self, request, queryset):
        queryset.update(is_call_for_project=True)
        self.message_user(request, _('The selected aids were set as CFP'))
    make_mark_as_CFP.short_description = _('Set as CFP')

    def show_export_message(self, request):
        self.message_user(request, get_admin_export_message())

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
            .prefetch_related('financers', 'instructors', 'perimeter') \
            .select_related('author', 'eligibility_test')
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
            .select_related('author', 'eligibility_test')
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
        qs = qs.select_related('author', 'eligibility_test')
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
