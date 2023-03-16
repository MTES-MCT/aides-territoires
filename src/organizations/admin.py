from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS
from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats

from organizations.models import Organization
from organizations.resources import OrganizationResource
from aids.constants import AUDIENCES_ALL


class OrganizationTypeListFilter(admin.SimpleListFilter):
    """Custom admin filter to target organizations with various types."""

    title = "Type d'organisation"
    parameter_name = "organization_type"

    def lookups(self, request, model_admin):
        return AUDIENCES_ALL

    def queryset(self, request, queryset):
        lookup_value = self.value()
        if lookup_value:
            queryset = queryset.filter(organization_type__contains=[lookup_value])
        return queryset


class OrganizationAdmin(ImportExportActionModelAdmin):

    resource_class = OrganizationResource
    formats = [base_formats.CSV, base_formats.XLSX]
    list_display = ["name", "date_created"]
    search_fields = ["name"]
    list_filter = [OrganizationTypeListFilter, "is_imported"]
    autocomplete_fields = ["beneficiaries", "backer", "perimeter", "favorite_projects"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = [
        "date_created",
        "date_updated",
        "get_projects",
        "population_strata",
    ]

    fieldsets = [
        (
            "",
            {
                "fields": (
                    "name",
                    "slug",
                    "organization_type",
                    "beneficiaries",
                    "backer",
                    "get_projects",
                    "favorite_projects",
                )
            },
        ),
        (
            "Informations sur la structure",
            {
                "fields": (
                    "perimeter",
                    "intercommunality_type",
                    "address",
                    "city_name",
                    "zip_code",
                    "siren_code",
                    "siret_code",
                    "ape_code",
                )
            },
        ),
        (
            "Chiffres clés",
            {
                "fields": (
                    ("inhabitants_number", "population_strata"),
                    "voters_number",
                    "corporates_number",
                    "shops_number",
                    "associations_number",
                    "municipal_roads",
                    "departmental_roads",
                    "tram_roads",
                    "lamppost_number",
                    "bridge_number",
                    "library_number",
                    "medialibrary_number",
                    "theater_number",
                    "cinema_number",
                    "museum_number",
                    "nursery_number",
                    "kindergarten_number",
                    "primary_school_number",
                    "rec_center_number",
                    "middle_school_number",
                    "high_school_number",
                    "university_number",
                    "tennis_court_number",
                    "football_field_number",
                    "running_track_number",
                    "other_outside_structure_number",
                    "covered_sporting_complex_number",
                    "swimming_pool_number",
                    "place_of_worship_number",
                    "cemetery_number",
                    "protected_monument_number",
                    "forest_number",
                )
            },
        ),
        (
            "Données diverses",
            {
                "fields": (
                    "date_created",
                    "date_updated",
                    "is_imported",
                    "imported_date",
                )
            },
        ),
    ]

    def get_projects(self, obj):
        projects = obj.project_set.all()
        projects_list = format_html("<table><tbody>")
        for project in projects:
            url = reverse("admin:projects_project_change", args=(project.pk,))
            projects_list += format_html(
                "<tr> \
                    <td><a href='{url}'>{project}</a></td> \
                <tr>",
                url=url,
                project=project.name,
            )
        projects_list += format_html("</tbody></table>")
        return projects_list

    get_projects.short_description = "Projets de la structure"

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
            "/static/js/search/enable_softmaxlength.js",
            "/static/trumbowyg/dist/trumbowyg.js",
            "/static/trumbowyg/dist/langs/fr.js",
            "/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js",
            "/static/jquery-resizable-dom/dist/jquery-resizable.js",
            "/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js",
            "/static/js/enable_rich_text_editor.js",
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS


admin.site.register(Organization, OrganizationAdmin)
