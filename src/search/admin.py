from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from search.models import SearchPage
from search.forms import SearchPageAdminForm
from pages.models import Page
from pages.admin import PageAdmin
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class HasAuthorFilter(admin.SimpleListFilter):
    """Custom admin filter to target search pages with authors."""

    title = _('Authors')
    parameter_name = 'has_authors'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.has_authors()
        elif value == 'No':
            return queryset.filter(author__isnull=True)
        return queryset


class HasContributorFilter(admin.SimpleListFilter):
    """Custom admin filter to target search pages with contributors."""

    title = _('Contributors')
    parameter_name = 'has_contributors'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.has_contributors()
        elif value == 'No':
            return queryset.filter(contributors__isnull=True)
        return queryset


class SearchPageAdmin(admin.ModelAdmin):
    form = SearchPageAdminForm
    list_display = ['slug', 'title', 'meta_description', 'date_created']
    filter_vertical = ['available_categories']
    search_fields = ['title']
    list_filter = [HasAuthorFilter, HasContributorFilter]

    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['author', 'contributors',
                           'highlighted_aids', 'excluded_aids']
    readonly_fields = [
        'all_aids_count', 'live_aids_count',
        'date_created', 'date_updated']

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
        ('Administration', {
            'fields': (
                'author',
                'contributors',
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
        ('Aides concernées', {
            'fields': (
                'all_aids_count',
                'live_aids_count'
            )
        }),
        ('Mettre en avant des aides', {
            'fields': (
                'highlighted_aids',
            )
        }),
        ('Exclure des aides des résultats', {
            'fields': (
                'excluded_aids',
            )
        }),
    ]

    def get_queryset(self, request):
        qs = super(admin.ModelAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.administrable_by_user(user=request.user)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields

        print(obj)
        print(request.user)
        print(request.user.is_superuser)
        print(readonly_fields)
        if obj and not request.user.is_superuser:
            self.prepopulated_fields = {}  # issue with 'slug' field instead
            readonly_fields += ['slug', 'querystring']
            if obj.author != request.user:
                readonly_fields += ['author']

        print(readonly_fields)
        return readonly_fields

    def all_aids_count(self, search_page):
        return search_page.get_base_queryset(all_aids=True).count()
    all_aids_count.short_description = "Nombre d'aides total (querystring)"

    def live_aids_count(self, search_page):
        live_aids_count = search_page.get_base_queryset().count()
        live_aids_local_count = search_page.get_base_queryset().local_aids().count()  # noqa
        return f'{live_aids_count} (dont aides locales : {live_aids_local_count})'  # noqa
    live_aids_count.short_description = "Nombre d'aides actuellement visibles"

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
