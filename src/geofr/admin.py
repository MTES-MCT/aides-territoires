from django import forms
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.urls import path

from admin_auto_filters.filters import AutocompleteFilter
from admin_numeric_filter.admin import NumericFilterModelAdmin, RangeNumericFilter

from exporting.tasks import export_perimeters_as_csv, export_perimeters_as_xlsx
from exporting.utils import get_admin_export_message

from geofr.admin_views import PerimeterUpload, PerimeterCombine
from geofr.models import FinancialData, Perimeter, PerimeterImport, PerimeterData
from geofr.utils import get_all_related_perimeters


class DepartmentFilter(admin.SimpleListFilter):
    """Custom admin filter to get perimeters by department."""

    parameter_name = "by_department"
    title = "Par département"
    template = "admin/dropdown_filter.html"

    def lookups(self, request, model_admin):
        return [(d.code, d.name) for d in Perimeter.objects.departments()]

    def queryset(self, request, queryset):
        value = self.value()

        if value:
            # Concatenating perimeters which either is the searched department
            # or a perimeter inside it (commune, EPCI)
            perimeter_is_dept = queryset.filter(
                scale=Perimeter.SCALES.department,
                code=value,
            )
            perimeter_in_dept = queryset.filter(departments__contains=[value])

            return perimeter_is_dept | perimeter_in_dept
        return queryset


class RegionFilter(admin.SimpleListFilter):
    """Custom admin filter to get perimeters by region."""

    parameter_name = "by_region"
    title = "Par région"
    template = "admin/dropdown_filter.html"

    def lookups(self, request, model_admin):
        return [(r.code, r.name) for r in Perimeter.objects.regions()]

    def queryset(self, request, queryset):
        value = self.value()

        if value:
            # Concatenating perimeters which either is the searched region
            # or a perimeter inside it (commune, EPCI, department)
            perimeter_is_region = queryset.filter(
                scale=Perimeter.SCALES.region,
                code=value,
            )
            perimeter_in_region = queryset.filter(regions__contains=[value])

            return perimeter_is_region | perimeter_in_region
        return queryset


class PerimeterAutocompleteFilter(AutocompleteFilter):
    field_name = "perimeter"
    title = "périmètre"

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            perimeter_ids = get_all_related_perimeters(value, values=["id"])
            return queryset.filter(perimeter__in=perimeter_ids)


class PerimeterDataInline(admin.TabularInline):
    model = PerimeterData
    extra = 0


class PerimeterAdminForm(forms.ModelForm):
    class Meta:
        fields = ["name", "code", "is_visible_to_users"]


class PerimeterAdmin(NumericFilterModelAdmin):
    """Admin module for perimeters."""

    form = PerimeterAdminForm
    list_display = [
        "scale",
        "name",
        "manually_created",
        "is_visible_to_users",
        "is_obsolete",
        "code",
        "is_overseas",
        "regions",
        "departments",
        "epci",
        "zipcodes",
        "basin",
    ]
    list_filter = [
        "scale",
        ("population", RangeNumericFilter),
        DepartmentFilter,
        RegionFilter,
        "is_overseas",
        "manually_created",
        "is_visible_to_users",
        "is_obsolete",
    ]
    search_fields = ["id", "name", "code"]
    ordering = ["-date_created"]
    actions = ["export_csv", "export_xlsx"]
    # readonly_fields are managed below

    inlines = [
        PerimeterDataInline,
    ]

    fieldsets = [
        (
            "",
            {
                "fields": (
                    "id",
                    ("name", "unaccented_name"),
                    "code",
                    "scale",
                    "manually_created",
                    ("is_obsolete", "date_obsolete"),
                    "is_visible_to_users",
                    "date_created",
                    "date_updated",
                )
            },
        ),
        (
            "Identifiants",
            {"fields": ("insee", "siren", "siret", "zipcodes")},
        ),
        (
            "Situation",
            {
                "fields": (
                    "continent",
                    "country",
                    "regions",
                    "departments",
                    "epci",
                    "basin",
                    "is_overseas",
                    ("latitude", "longitude"),
                )
            },
        ),
        (
            "Données",
            {
                "fields": (
                    "population",
                    "surface",
                    "density_typology",
                )
            },
        ),
        (
            "Compteurs",
            {
                "fields": (
                    "backers_count",
                    "programs_count",
                    "projects_count",
                    "live_aids_count",
                    "categories_count",
                )
            },
        ),
    ]

    class Media:
        css = {"all": ("css/admin.css",)}

    def get_readonly_fields(self, request, obj=None):
        """
        All fields are readonly except:
        - Allow name is_visible_to_users edition for new or adhoc perimeters
        - Allow code edition for new or manually_created perimeters
        """
        readonly_fields = [f.name for f in Perimeter._meta.fields]
        if not obj or (obj.scale == Perimeter.SCALES.adhoc):
            readonly_fields.remove("name")
            readonly_fields.remove("is_visible_to_users")
        if not obj or obj.manually_created:
            readonly_fields.remove("code")
        return readonly_fields

    def get_changeform_initial_data(self, request):
        """Set is_visible_to_users to False for new perimeters"""
        initial = super(PerimeterAdmin, self).get_changeform_initial_data(
            request
        )  # noqa
        initial["is_visible_to_users"] = False
        return initial

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj and request.user.is_superuser:
            return obj.manually_created
        return False

    def save_model(self, request, obj, form, change):
        """Handle perimeter manual creations.

        Only adhoc perimeters can be created. Other perimeters are imported
        from the geo api or other official data sources.
        """
        obj.manually_created = True
        obj.scale = Perimeter.SCALES.adhoc
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Add France and Europe perimeters to new adhoc perimeters."""

        if not change:
            perimeters = Perimeter.objects.filter(
                scale__in=(Perimeter.SCALES.continent, Perimeter.SCALES.country)
            )
            obj = form.instance
            obj.contained_in.add(*perimeters)

        super().save_related(request, form, formsets, change)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "<path:object_id>/upload/",
                self.admin_site.admin_view(self.perimeter_upload_view),
                name="geofr_perimeter_upload",
            ),
            path(
                "<path:object_id>/combiner/",
                self.admin_site.admin_view(self.perimeter_combine_view),
                name="geofr_perimeter_combine",
            ),
        ]
        return my_urls + urls

    def perimeter_upload_view(self, request, object_id=None):
        """Display the form to upload a list of communes."""

        opts = self.model._meta
        app_label = opts.app_label
        obj = self.get_object(request, object_id)

        context = {
            **self.admin_site.each_context(request),
            "title": "Upload de périmètre",
            "opts": opts,
            "app_label": app_label,
            "original": obj,
        }
        return PerimeterUpload.as_view(extra_context=context)(
            request, object_id=object_id
        )

    def perimeter_combine_view(self, request, object_id=None):
        """Display the form to combine several perimeters."""

        opts = self.model._meta
        app_label = opts.app_label
        obj = self.get_object(request, object_id)

        context = {
            **self.admin_site.each_context(request),
            "title": "Combinaison de périmètre",
            "opts": opts,
            "app_label": app_label,
            "original": obj,
        }
        return PerimeterCombine.as_view(extra_context=context)(
            request, object_id=object_id
        )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        contained_perimeters = Perimeter.objects.filter(
            contained_in__id=object_id
        ).order_by("-scale", "name")
        context = extra_context or {}
        context["contained_perimeters"] = contained_perimeters

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=context
        )

    def show_export_message(self, request):
        self.message_user(request, get_admin_export_message())

    def export_csv(self, request, queryset):
        perimeters_id_list = list(queryset.values_list("id", flat=True))
        export_perimeters_as_csv.delay(perimeters_id_list, request.user.id)
        self.show_export_message(request)

    export_csv.short_description = (
        "Exporter les périmètres sélectionnés en CSV en tâche de fond"
    )

    def export_xlsx(self, request, queryset):
        perimeters_id_list = list(queryset.values_list("id", flat=True))
        export_perimeters_as_xlsx.delay(perimeters_id_list, request.user.id)
        self.show_export_message(request)

    export_xlsx.short_description = (
        "Exporter les périmètres sélectionnés en XLSX en tâche de fond"
    )


class PerimeterImportAdmin(admin.ModelAdmin):
    """Admin module for perimeters."""

    list_display = [
        "__str__",
        "adhoc_perimeter",
        "is_imported",
        "date_imported",
        "date_created",
        "date_updated",
    ]
    list_filter = ["is_imported"]
    search_fields = ["id", "__str__", "adhoc_perimeter__name"]
    ordering = ["-date_created"]
    raw_id_fields = ("adhoc_perimeter", "author")
    formfield_overrides = {
        ArrayField: dict(widget=forms.Textarea(attrs=dict(readonly=True)))
    }
    readonly_fields = ["perimeters_count", "date_created", "date_updated"]
    fieldsets = (
        (None, {"fields": ("adhoc_perimeter", "author")}),
        (
            "Périmètres à attacher",
            {
                "fields": ("city_codes", "perimeters_count"),
            },
        ),
        (
            "Import",
            {
                "fields": ("is_imported", "date_imported"),
            },
        ),
        (
            "Métadonnées",
            {
                "fields": ("date_created", "date_updated"),
            },
        ),
    )

    def perimeters_count(self, obj):
        """Number of perimeters to attach"""
        if obj.city_codes is not None:
            return len(obj.city_codes)
        else:
            return 0

    perimeters_count.short_description = "Nombre de périmètres"
    perimeters_count.help_text = "Nombre de périmètres à attacher"


class FinancialDataAdmin(admin.ModelAdmin):
    """Admin module for financial data."""

    list_display = [
        "short_perimeter_name",
        "year",
        "aggregate",
        "formatted_main_budget_amount",
    ]
    list_filter = [PerimeterAutocompleteFilter, "year", "aggregate"]

    def formatted_main_budget_amount(self, obj):
        return f"{obj.main_budget_amount:,.2f} €".replace(",", " ").replace(".", ",")

    formatted_main_budget_amount.short_description = "montant budget principal"
    formatted_main_budget_amount.admin_order_field = "main_budget_amount"

    def short_perimeter_name(self, obj):
        perimeter_name = str(obj.perimeter)

        if len(perimeter_name) >= 100:
            perimeter_name = f"{perimeter_name[:98]}[...]{perimeter_name[-1]}"
        return perimeter_name

    short_perimeter_name.short_description = "commune"
    short_perimeter_name.admin_order_field = "perimeter__insee"


admin.site.register(Perimeter, PerimeterAdmin)
admin.site.register(PerimeterImport, PerimeterImportAdmin)
admin.site.register(FinancialData, FinancialDataAdmin)
