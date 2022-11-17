import re
from functools import reduce
from operator import and_

from django.db.models import Q
from django.contrib import admin
from django.http import HttpResponseForbidden

from import_export.admin import ImportMixin, ExportActionMixin
from import_export.formats import base_formats
from admin_auto_filters.filters import AutocompleteFilter
from fieldsets_with_inlines import FieldsetsInlineMixin
from adminsortable2.admin import SortableInlineAdminMixin

from core.services.json_compare import json_compare
from accounts.admin import AuthorFilter
from admin_lite.mixins import WithViewPermission
from aids.forms import AidAdminForm
from aids.models import (
    Aid,
    AidWorkflow,
    AidFinancer,
    AidInstructor,
    AidProject,
    SuggestedAidProject,
)
<<<<<<< HEAD
from aids.resources import AidResource, AidProjectResource
from aids.utils import generate_clone_title
=======
from aids.resources import AidResource
>>>>>>> 19da4072... remove generate_clone_title method
from core.admin import InputFilter, pretty_print_readonly_jsonfield
from core.constants import YES_NO_CHOICES
from exporting.tasks import (
    export_aids_as_csv,
    export_aids_as_xlsx,
    export_aidprojects_as_csv,
    export_aidprojects_as_xlsx,
)
from exporting.utils import get_admin_export_message
from geofr.utils import get_all_related_perimeters
from search.models import SearchPage
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class LiveAidListFilter(admin.SimpleListFilter):
    """Custom admin filter to target aids with various statuses."""

    title = "État"
    parameter_name = "state"

    def lookups(self, request, model_admin):
        return (
            # aid.state
            ("open", "Aides ouvertes"),
            ("deadline", "Expirent bientôt"),
            ("expired", "Aides expirées"),
            # aid.display_status
            ("hidden", "Actuellement non affichées"),
            ("live", "Actuellement affichées"),
        )

    def queryset(self, request, queryset):
        if self.value() == "open":
            return queryset.open()

        if self.value() == "expired":
            return queryset.expired()

        if self.value() == "deadline":
            return queryset.soon_expiring()

        if self.value() == "hidden":
            return queryset.hidden()

        if self.value() == "live":
            return queryset.published().open()


class EligibilityTestFilter(admin.SimpleListFilter):
    """Custom admin filter to target aids with eligibility tests."""

    title = "Test d'éligibilité"
    parameter_name = "has_eligibility_test"

    def lookups(self, request, model_admin):
        return YES_NO_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.has_eligibility_test()
        elif value == "No":
            return queryset.filter(eligibility_test__isnull=True)
        return queryset


class GenericAidListFilter(admin.SimpleListFilter):
    """Custom admin filter for generic, local and standard aids."""

    title = "Générique / Locale"
    parameter_name = "typology"

    def lookups(self, request, model_admin):
        return (
            ("generic", "Aides génériques"),
            ("local", "Local aids"),
            ("standard", "Standard aids"),
        )

    def queryset(self, request, queryset):
        if self.value() == "generic":
            return queryset.generic_aids()

        if self.value() == "local":
            return queryset.local_aids()

        if self.value() == "standard":
            return queryset.standard_aids()


class BackersFilter(InputFilter):
    parameter_name = "backers"
    title = "Porteurs d’aides"

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            bits = value.split(" ")
            financer_filters = [Q(financers__name__icontains=bit) for bit in bits]
            instructor_filters = [Q(instructors__name__icontains=bit) for bit in bits]
            return queryset.filter(
                Q(reduce(and_, financer_filters)) | Q(reduce(and_, instructor_filters))
            )


class PerimeterFilter(InputFilter):
    parameter_name = "perimeter"
    title = "Périmètre"

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            return queryset.filter(Q(perimeter__name__icontains=value))


class PerimeterAutocompleteFilter(AutocompleteFilter):
    field_name = "perimeter"
    title = "Périmètre"

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            perimeter_ids = get_all_related_perimeters(value, values=["id"])
            return queryset.filter(perimeter__in=perimeter_ids)


class FinancersInline(SortableInlineAdminMixin, admin.TabularInline):
    """Configure the formset to the financers m2m field."""

    model = AidFinancer
    extra = 1
    verbose_name = "Porteur d’aide"
    verbose_name_plural = "Porteurs d’aides"
    autocomplete_fields = ["backer"]


class InstructorsInline(SortableInlineAdminMixin, admin.TabularInline):
    """Configure the formset to the instructors m2m field."""

    model = AidInstructor
    extra = 1
    verbose_name = "Instructeur"
    verbose_name_plural = "Instructeurs"
    autocomplete_fields = ["backer"]


class BaseAidAdmin(
    FieldsetsInlineMixin, ImportMixin, ExportActionMixin, admin.ModelAdmin
):
    """Admin module for aids."""

    form = AidAdminForm
    resource_class = AidResource
    ordering = ["-id"]
    save_as = True
    actions = ["export_csv", "export_xlsx", "export_admin_action", "make_mark_as_CFP"]
    formats = [base_formats.CSV, base_formats.XLSX]
    list_display = [
        "live_status",
        "name",
        "all_financers",
        "all_instructors",
        "author_name",
        "recurrence",
        "perimeter",
        "date_updated",
        "date_published",
        "is_imported",
        "import_last_access",
        "submission_deadline",
        "status",
    ]
    list_display_links = ["name"]
    search_fields = ["id", "name", "name_initial"]
    list_filter = [
        "status",
        LiveAidListFilter,
        GenericAidListFilter,
        "recurrence",
        "is_imported",
        "import_data_source",
        "is_call_for_project",
        "in_france_relance",
        EligibilityTestFilter,
        AuthorFilter,
        BackersFilter,
        PerimeterAutocompleteFilter,
        "programs",
        "categories__theme",
        "categories",
    ]

    autocomplete_fields = [
        "author",
        "financers",
        "instructors",
        "perimeter",
        "programs",
        "keywords",
    ]
    filter_vertical = [
        "categories",
    ]  # Overriden in the widget definition
    readonly_fields = [
        "sibling_aids",
        "is_imported",
        "import_data_source",
        "import_uniqueid",
        "import_data_mention",
        "import_data_url",
        "import_share_licence",
        "import_last_access",  # noqa
        "get_pprint_import_raw_object",
        "get_pprint_import_raw_object_calendar",
        "get_pprint_import_raw_object_temp",
        "get_pprint_import_raw_object_temp_calendar",
        "import_raw_object_diff",
        "import_raw_object_calendar_diff",
        "date_created",
        "date_updated",
        "date_published",
    ]
    raw_id_fields = ["generic_aid"]

    fieldsets_with_inlines = [
        (
            "Présentation de l'aide",
            {
                "fields": (
                    "name",
                    "slug",
                    "in_france_relance",
                    "european_aid",
                    "name_initial",
                    "short_title",
                    "categories",
                    "targeted_audiences",
                    "author",
                    "sibling_aids",
                )
            },
        ),
        FinancersInline,
        ("PORTEURS D'AIDES SUGGÉRÉS", {"fields": ("financer_suggestion",)}),
        InstructorsInline,
        ("INSTRUCTEURS SUGGÉRÉS", {"fields": ("instructor_suggestion",)}),
        (
            "Périmètre de l'aide",
            {
                "fields": (
                    "perimeter",
                    "perimeter_suggestion",
                )
            },
        ),
        (
            "Calendrier de l'aide",
            {
                "fields": (
                    "recurrence",
                    "start_date",
                    "predeposit_date",
                    "submission_deadline",
                )
            },
        ),
        (
            "Description de l'aide",
            {
                "fields": (
                    "is_call_for_project",
                    "programs",
                    "aid_types",
                    "subvention_rate",
                    "subvention_comment",
                    "loan_amount",
                    "recoverable_advance_amount",
                    "other_financial_aid_comment",
                    "mobilization_steps",
                    "destinations",
                    "description",
                    "project_examples",
                    "eligibility",
                    "keywords",
                )
            },
        ),
        (
            "Contact et démarches",
            {
                "fields": (
                    "origin_url",
                    "application_url",
                    "contact",
                )
            },
        ),
        ("Éligibilité", {"fields": ("eligibility_test",)}),
        (
            "Administration de l'aide",
            {
                "fields": (
                    "status",
                    "author_notification",
                )
            },
        ),
        ("Uniquement pour les aides génériques", {"fields": ("is_generic",)}),
        (
            "Uniquement pour les aides locales",
            {
                "fields": (
                    "generic_aid",
                    "local_characteristics",
                )
            },
        ),
        (
            "Données liées à l'import",
            {
                "fields": (
                    "is_imported",
                    "import_data_source",
                    "import_uniqueid",
                    "import_data_mention",
                    "import_data_url",
                    "import_share_licence",
                    "import_last_access",
                    "get_pprint_import_raw_object",
                    "get_pprint_import_raw_object_temp",
                    "import_raw_object_diff",
                    "get_pprint_import_raw_object_calendar",
                    "get_pprint_import_raw_object_temp_calendar",
                    "import_raw_object_calendar_diff",
                )
            },
        ),
        (
            "Données diverses",
            {
                "fields": (
                    "date_created",
                    "date_updated",
                    "date_published",
                )
            },
        ),
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            # Non-superuser are not allow to run actions.
            actions = []
        return actions

    def get_search_results(self, request, queryset, search_term):
        """
        Here we can override the result of 'aids' autocomplete_fields
        used in other admins.
        Usage:
        - autocomplete_fields is used on 'highlighted_aids' in the SearchPage
        admin. But we want to restrict the queryset to only the SearchPage aids
        """

        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        # e.g. '<host>/admin/search/searchpage/35/change/'
        meta_http_referer = request.META.get("HTTP_REFERER", "")
        # e.g. 'app_label=search&model_name=searchpage&field_name=highlighted_aids'
        meta_query_string = request.META.get("QUERY_STRING", "")

        # custom SearchPage.highlighted_aids autocomplete filter
        if meta_query_string and all(
            x in meta_query_string for x in ["searchpage", "highlighted_aids"]
        ):  # noqa
            try:
                search_page_id_str = re.search(
                    "searchpage/(.*?)/change", meta_http_referer
                ).group(
                    1
                )  # noqa
                queryset = SearchPage.objects.get(
                    pk=int(search_page_id_str)
                ).get_base_queryset(all_aids=True)
            except AttributeError:  # regex error
                pass

        return queryset, use_distinct

    def change_view(self, request, object_id, extra_context=None):
        """
        We prevent non-superuser to acces this page. Permission is given to list
        aids in contributor admin pages, but we don't give them direct access to
        aid admin pages.
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super().change_view(request, object_id, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        """
        We prevent non-superuser to acces this page.
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super().changelist_view(request, extra_context=extra_context)

    def sibling_aids(self, aid):
        """Number of other (non draft) aids created by the same author."""

        return (
            Aid.objects.exclude(id=aid.id)
            .filter(author=aid.author)
            .filter(status__in=("reviewable", "published"))
            .count()
        )

    sibling_aids.short_description = "Du même auteur"
    sibling_aids.help_text = (
        "Nb. d'autres aides (sauf brouillons) créées par le même utilisateur"
    )

    def get_form(self, request, obj=None, **kwargs):
        """Set readonly fields help texts."""
        help_texts = {"sibling_aids": self.sibling_aids.help_text}
        kwargs.update({"help_texts": help_texts})
        return super().get_form(request, obj, **kwargs)

    def author_name(self, aid):
        if aid.author is not None:
            return aid.author.full_name

    author_name.short_description = "Auteur"

    def all_financers(self, aid):
        financers = [backer.name for backer in aid.financers.all()]
        return ", ".join(financers)

    all_financers.short_description = "Porteurs d'aides"

    def all_instructors(self, aid):
        instructors = [backer.name for backer in aid.instructors.all()]
        return ", ".join(instructors)

    all_instructors.short_description = "Instructeurs"

    def live_status(self, aid):
        return aid.is_live()

    live_status.boolean = True
    live_status.short_description = "Live"

    def has_eligibility_test(self, aid):
        return aid.has_eligibility_test()

    has_eligibility_test.boolean = True
    has_eligibility_test.short_description = "Test d'éligibilité"

    def get_pprint_import_raw_object(self, obj=None):
        if obj:
            return pretty_print_readonly_jsonfield(obj.import_raw_object)
        return ""

    get_pprint_import_raw_object.short_description = "Donnée brute importée"

    def get_pprint_import_raw_object_calendar(self, obj=None):
        if obj:
            return pretty_print_readonly_jsonfield(obj.import_raw_object_calendar)
        return ""

    get_pprint_import_raw_object_calendar.short_description = (
        "Donnée brute importée pour le calendrier"  # noqa
    )

    def get_pprint_import_raw_object_temp(self, obj=None):
        if obj:
            return pretty_print_readonly_jsonfield(obj.import_raw_object_temp)
        return ""

    get_pprint_import_raw_object_temp.short_description = (
        "Donnée brute importée temporaire"
    )

    def get_pprint_import_raw_object_temp_calendar(self, obj=None):
        if obj:
            return pretty_print_readonly_jsonfield(obj.import_raw_object_temp_calendar)
        return ""

    get_pprint_import_raw_object_temp_calendar.short_description = (
        "Donnée brute importée temporaire pour le calendrier"  # noqa
    )

    def import_raw_object_diff(self, obj):
        return json_compare(obj.import_raw_object, obj.import_raw_object_temp)

    import_raw_object_diff.short_description = (
        "Modifications de la donnée brute importée"
    )

    def import_raw_object_calendar_diff(self, obj):
        return json_compare(
            obj.import_raw_object_calendar, obj.import_raw_object_calendar_temp
        )

    import_raw_object_calendar_diff.short_description = (
        "Modifications de la donnée brute importée pour le calendrier"  # noqa
    )

    def make_mark_as_CFP(self, request, queryset):
        queryset.update(is_call_for_project=True)
        self.message_user(
            request, "Les aides sélectionnées ont été marquées en tant qu'AAP"
        )

    make_mark_as_CFP.short_description = "Marquer en tant qu'AAP"

    def show_export_message(self, request):
        self.message_user(request, get_admin_export_message())

    def export_csv(self, request, queryset):
        aids_id_list = list(queryset.values_list("id", flat=True))
        export_aids_as_csv.delay(aids_id_list, request.user.id)
        self.show_export_message(request)

    export_csv.short_description = (
        "Exporter les Aides sélectionnées en CSV en tâche de fond"
    )

    def export_xlsx(self, request, queryset):
        aids_id_list = list(queryset.values_list("id", flat=True))
        export_aids_as_xlsx.delay(aids_id_list, request.user.id)
        self.show_export_message(request)

    export_xlsx.short_description = (
        "Exporter les Aides sélectionnées en XLSX en tâche de fond"
    )

    def export_admin_action(self, request, queryset):
        # We do a noop override of this method, just because
        # we want to customize it's short description
        return super().export_admin_action(request, queryset)

    export_admin_action.short_description = (
        "Exporter et télécharger les Aides sélectionnées"
    )

    def save_model(self, request, obj, form, change):
        if obj.import_raw_object_temp:
            obj.import_raw_object = obj.import_raw_object_temp
            obj.import_raw_object_temp = None

        if obj.import_raw_object_temp_calendar:
            obj.import_raw_object_calendar = obj.import_raw_object_temp_calendar
            obj.import_raw_object_temp_calendar = None

        super(BaseAidAdmin, self).save_model(request, obj, form, change)

    class Media:
        css = {
            "all": (
                "/static/css/admin.css",
                "/static/trumbowyg/dist/ui/trumbowyg.css",
            )
        }
        js = [
            "admin/js/jquery.init.js",
            "/static/js/shared_config.js",
            "/static/js/plugins/softmaxlength.js",
            "/static/js/aids/enable_softmaxlength.js",
            "/static/trumbowyg/dist/trumbowyg.js",
            "/static/trumbowyg/dist/langs/fr.js",
            "/static/js/enable_rich_text_editor.js",
            "/static/js/aids/duplicate_buster.js",
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS


class AidAdmin(WithViewPermission, BaseAidAdmin):
    def get_queryset(self, request):
        qs = (
            Aid.objects.all()
            .distinct()
            .prefetch_related("financers", "instructors", "perimeter")
            .select_related("author", "eligibility_test")
        )
        return qs

    def delete_model(self, request, obj):
        obj.soft_delete()

    def delete_queryset(self, request, queryset):
        queryset.update(status="deleted")

    def save_model(self, request, obj, form, change):
        # When cloning an existing aid, prefix it's title with "[Copie]"
        if "_saveasnew" in request.POST:
            obj.status = AidWorkflow.states.draft
        return super().save_model(request, obj, form, change)


class DeletedAid(Aid):
    class Meta:
        proxy = True
        verbose_name = "Aide supprimée"
        verbose_name_plural = "Aides supprimées"


class DeletedAidAdmin(BaseAidAdmin):
    def get_queryset(self, request):
        qs = (
            Aid.deleted_aids.all()
            .prefetch_related("financers", "instructors")
            .select_related("author", "eligibility_test")
        )
        return qs


class Amendment(Aid):
    """We need this so we can register the same model twice."""

    class Meta:
        proxy = True
        verbose_name = "Amendement"
        verbose_name_plural = "Amendements"


class AmendmentAdmin(admin.ModelAdmin):
    list_display = ["name", "amended_aid", "amendment_author_name", "date_created"]

    def get_queryset(self, request):
        qs = Aid.amendments.all()
        qs = qs.prefetch_related("financers")
        qs = qs.select_related("author", "eligibility_test")
        return qs


class AidProjectStatusFilter(admin.SimpleListFilter):
    title = "Statut de l'aide par rapport au projet"
    parameter_name = "aidproject_status"

    def lookups(self, request, model_admin):
        return [
            ("filled", "Renseigné"),
            ("not_filled", "Non renseigné"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "filled":
            # Get aidproject objects where aid has been requested.
            return queryset.distinct().filter(aid_requested=True)
        if self.value() == "not_filled":
            # Get aidproject objects where aid has not been requested.
            return queryset.distinct().filter(aid_requested=False)


class AidProjectAdmin(admin.ModelAdmin):
    resource_class = AidProjectResource
    ordering = ["-id"]
    actions = ["export_csv", "export_xlsx"]
    formats = [base_formats.CSV, base_formats.XLSX]

    list_display = [
        "aid",
        "project",
        "creator",
        "aid_obtained",
        "aid_requested",
        "aid_paid",
        "aid_denied",
        "date_created",
    ]
    list_filter = [
        AidProjectStatusFilter,
        "aid_obtained",
        "aid_requested",
        "aid_paid",
        "aid_denied",
    ]
    readonly_fields = [
        "aid",
        "project",
        "creator",
        "aid_requested",
        "date_requested",
        "aid_obtained",
        "date_obtained",
        "aid_denied",
        "date_denied",
        "aid_paid",
        "date_paid",
        "date_created",
    ]

    def show_export_message(self, request):
        self.message_user(request, get_admin_export_message())

    def export_csv(self, request, queryset):
        aidprojects_id_list = list(queryset.values_list("id", flat=True))
        export_aidprojects_as_csv.delay(aidprojects_id_list, request.user.id)
        self.show_export_message(request)

    export_csv.short_description = (
        "Exporter les objets aidproject sélectionnés en CSV en tâche de fond"
    )

    def export_xlsx(self, request, queryset):
        aidprojects_id_list = list(queryset.values_list("id", flat=True))
        export_aidprojects_as_xlsx.delay(aidprojects_id_list, request.user.id)
        self.show_export_message(request)

    export_xlsx.short_description = (
        "Exporter les objets aidproject sélectionnés en XLSX en tâche de fond"
    )


class SuggestedAidProjectAdmin(admin.ModelAdmin):
    list_display = ["aid", "project", "is_associated", "is_rejected", "date_created"]
    readonly_fields = [
        "aid",
        "project",
        "creator",
        "is_associated",
        "is_rejected",
        "date_created",
        "date_associated",
        "date_rejected",
    ]


admin.site.register(Aid, AidAdmin)
admin.site.register(DeletedAid, DeletedAidAdmin)
admin.site.register(Amendment, AmendmentAdmin)
admin.site.register(AidProject, AidProjectAdmin)
admin.site.register(SuggestedAidProject, SuggestedAidProjectAdmin)
