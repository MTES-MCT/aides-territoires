from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from search.forms import SearchPageAdminForm
from search.models import SearchPage
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class SearchPageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    form = SearchPageAdminForm
    filter_vertical = ['available_categories']

    fieldsets = [
        ('', {
            'fields': (
                'title',
                'short_title',
                'slug',
                'search_querystring',
                'content',
                'more_content',
            )
        }),
        (_('SEO'), {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_image',
            )
        }),
        (_('Style customization'), {
            'fields': (
                'logo',
                'logo_link',
                'color_1',
                'color_2',
                'color_3',
                'color_4',
                'color_5',
            )
        }),
        (_('Form customization'), {
            'fields': (
                'show_categories_field',
                'available_categories',
                'show_audience_field',
                'available_audiences',
                'show_perimeter_field',
                'show_mobilization_step_field',
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


admin.site.register(SearchPage, SearchPageAdmin)
