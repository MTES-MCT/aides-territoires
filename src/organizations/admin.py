from django.contrib import admin
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS
from organizations.models import Organization


class OrganizationAdmin(admin.ModelAdmin):

    list_display = ['name','date_created']
    search_fields = ['name']
    list_filter = ['name']
    autocomplete_fields = ['beneficiaries',
                           'perimeter']

    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['date_created', 'date_updated']

    fieldsets = [
        ('', {
            'fields': (
                'name',
                'slug',
                'organization_type',
                'perimeter',
                'beneficiaries',
                'projects',
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
