from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from search.models import SearchPage
from search.forms import SearchPageAdminForm


class SearchPageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    form = SearchPageAdminForm
    filter_vertical = ['available_categories']

    fieldsets = [
        ('', {
            'fields': (
                'title',
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
                'available_categories',
                'show_perimeter_field',
                'show_audiance_field',
                'show_categories_field',
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
            '/static/js/enable_rich_text_editor.js',
        ]


admin.site.register(SearchPage, SearchPageAdmin)
