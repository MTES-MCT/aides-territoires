from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from search.models import SearchPage
from search.forms import SearchPageAdminForm


class SearchPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    form = SearchPageAdminForm

    fieldsets = [
        ('', {
            'fields': (
                'title',
                'slug',
                'search_querystring',
                'content',
            )
        }),
        (_('SEO'), {
            'fields': (
                'meta_title',
                'meta_description',
            )
        }),
        (_('Customization'), {
            'fields': (
                'logo',
                'logo_link',
                'color_1',
                'color_2',
                'color_3',
                'color_4',
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
