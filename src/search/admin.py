from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm

from core.forms import RichTextField
from search.models import SearchPage
from search.forms import SearchPageAdminForm
from pages.models import Page
from pages.admin import PageForm, PageAdmin
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class SearchPageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'meta_description', 'date_created']
    form = SearchPageAdminForm
    prepopulated_fields = {'slug': ('title',)}
    filter_vertical = ['available_categories']
    autocomplete_fields = ['excluded_aids']
    readonly_fields = ['date_created', 'date_updated']
    search_fields = ['title']
    fieldsets = [
        ('', {
            'fields': (
                'title',
                'short_title',
                'slug',
                'search_querystring',
                'content',
                'more_content',
                'date_created',
                'date_updated',
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
                'show_aid_type_field',
            )
        }),
        (_('Exclude aids from results'), {
            'fields': (
                'excluded_aids',
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


# Dummy class so the model can be registered twice
class MinisitePage(Page):
    class Meta:
        proxy = True
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class MinisitePageAdmin(PageAdmin):

    HELP = _("WARNING! DON'T CHANGE url of pages in the main menu.")

    fieldsets = (
        (None, {
            'fields': ('url', 'minisite', 'title', 'content'),
            'description': '<div class="help">{}</div>'.format(HELP)}),
        (_('SEO'), {'fields': (
            'meta_title', 'meta_description')})
    )
    autocomplete_fields = ['minisite']
    list_display = ['url', 'title', 'minisite']

    def get_queryset(self, request):
        qs = Page.objects \
            .minisite_pages() \
            .select_related('minisite')
        return qs


admin.site.register(SearchPage, SearchPageAdmin)
admin.site.register(MinisitePage, MinisitePageAdmin)
