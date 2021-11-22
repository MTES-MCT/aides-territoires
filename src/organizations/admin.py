from django.contrib import admin
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS
from organizations.models import Organization
from aids.constants import AUDIENCES_ALL


class OrganizationTypeListFilter(admin.SimpleListFilter):
    """Custom admin filter to target organizations with various types."""

    title = "Type d'organisation"
    parameter_name = 'organization_type'

    def lookups(self, request, model_admin):
        return AUDIENCES_ALL

    def queryset(self, request, queryset):
        lookup_value = self.value()
        if lookup_value:
            queryset = queryset.filter(organization_type__contains=[lookup_value])
        return queryset


class OrganizationAdmin(admin.ModelAdmin):

    list_display = ['name', 'date_created']
    search_fields = ['name']
    list_filter = [OrganizationTypeListFilter]
    autocomplete_fields = ['beneficiaries',
                           'perimeter', 'projects']

    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['date_created', 'date_updated']

    fieldsets = [
        ('', {
            'fields': (
                'name',
                'slug',
                'organization_type',
                'beneficiaries',
                'projects',
            )
        }),
        ('Informations sur la structure', {
            'fields': (
                'perimeter',
                'address',
                'city_name',
                'zip_code',
                'siren_code',
                'siret_code',
                'ape_code',
            )
        }),
        ('Chiffres clés', {
            'fields': (
                'inhabitants_number',
                'voters_number',
                'corporates_number',
                'associations_number',
                'municipal_roads',
                'departmental_roads',
                'tram_roads',
                'lamppost_number',
                'library_number',
                'medialibrary_number',
                'theater_number',
                'museum_number',
                'kindergarten_number',
                'primary_school_number',
                'middle_school_number',
                'high_school_number',
                'university_number',
                'gymnasium_number',
                'sports_ground_number',
                'swimming_pool_number',
                'place_of_worship_number',
                'cemetery_number',
            )
        }),
        ('Données diverses', {
            'fields': (
                'date_created',
                'date_updated',
            )
        }),
    ]

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
            '/static/js/search/enable_softmaxlength.js',
            '/static/trumbowyg/dist/trumbowyg.js',
            '/static/trumbowyg/dist/langs/fr.js',
            '/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js',
            '/static/trumbowyg/dist/plugins/resizimg/resizable-resolveconflict.js',  # noqa
            '/static/jquery-resizable-dom/dist/jquery-resizable.js',
            '/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js',
            '/static/js/enable_rich_text_editor.js',
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS


admin.site.register(Organization, OrganizationAdmin)
