from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from fieldsets_with_inlines import FieldsetsInlineMixin

from admin_lite.mixins import AdminLiteMixin
from search.models import SearchPage, SearchPageLite
from search.forms import SearchPageAdminForm
from pages.models import Page
from pages.admin import PageForm, PageAdmin
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class MinisitePage(Page):
    """
    Proxy class to make Page model available for minisites.
    A minisite's page can be seen as a tab for the minisite.
    """
    class Meta:
        proxy = True
        verbose_name = "onglet de la page"
        verbose_name_plural = "onglets de la page"


class MinisitePageInline(admin.TabularInline):
    model = MinisitePage
    form = PageForm  # to display 'content' as RichTextField
    fields = ['url', 'title', 'content']
    extra = 1


class MinisitePageLiteInline(MinisitePageInline):
    """
    A lite version that's suitable for non superuser.
    """
    pass


BASE_FIELDSETS_SEARCH_PAGE = [
        ('', {
            'fields': (
                'title',
                'content',
                'more_content',
            )
        }),
        ('À propos de cette page', {
            'fields': (
                'date_created',
                'date_updated',
                'all_aids_count',
                'live_aids_count'
            )
        }),
        ('Personnalisation du style', {
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
        ('Personnalisation du formulaire', {
            'description': 'Maximum de 3 cases à cocher',
            'fields': (
                'show_categories_field',
                'available_categories',
                'show_audience_field',
                'available_audiences',
                'show_perimeter_field',
                'show_mobilization_step_field',
                'show_aid_type_field',
                'show_backers_field',
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

# For the lite admin, we want the lite version of MinistePage
LITE_FIELDSETS_SEARCH_PAGE = BASE_FIELDSETS_SEARCH_PAGE.copy()
LITE_FIELDSETS_SEARCH_PAGE.append(MinisitePageLiteInline)

# For superusers, we want to add more admin sections.
SUPERUSER_FIELDSETS_SEARCH_PAGE = BASE_FIELDSETS_SEARCH_PAGE.copy()
SUPERUSER_FIELDSETS_SEARCH_PAGE.insert(1, ('Configuration', {
    'fields': (
        'administrator',
        'short_title',
        'slug',
        'search_querystring',
    )})
)
SUPERUSER_FIELDSETS_SEARCH_PAGE.insert(3, ('SEO', {
    'fields': (
        'meta_title',
        'meta_description',
        'meta_image',
    )
})
)
SUPERUSER_FIELDSETS_SEARCH_PAGE.append(MinisitePageInline)


class AdministratorFilter(admin.SimpleListFilter):
    """Custom admin filter to target search pages with administrators."""

    title = 'Administrateur ?'
    parameter_name = 'has_administrator'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.has_administrators()
        elif value == 'No':
            return queryset.filter(administrator__isnull=True)
        return queryset


class SearchPageAdmin(FieldsetsInlineMixin, admin.ModelAdmin):
    list_display = ['slug', 'title', 'meta_description', 'nb_pages', 'date_created']
    filter_vertical = ['available_categories']
    search_fields = ['title']
    list_filter = [AdministratorFilter]

    form = SearchPageAdminForm
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['administrator',
                           'highlighted_aids', 'excluded_aids']
    readonly_fields = [
        'all_aids_count', 'live_aids_count',
        'date_created', 'date_updated']

    fieldsets_with_inlines = SUPERUSER_FIELDSETS_SEARCH_PAGE

    def get_queryset(self, request):
        qs = super().get_queryset(request).for_user(request.user)
        qs = qs.annotate(page_count=Count('pages'))
        return qs

    def get_list_filter(self, request):
        list_filter = self.list_filter

        if request.user.is_superuser:
            return list_filter

        return []

    def nb_pages(self, search_page):
        return search_page.page_count
    nb_pages.short_description = 'Nombre de pages'
    nb_pages.admin_order_field = 'page_count'

    def all_aids_count(self, search_page):
        return search_page.get_base_queryset(all_aids=True).count()
    all_aids_count.short_description = "Nombre d'aides total (querystring)"

    def live_aids_count(self, search_page):
        live_aids_count = search_page.get_base_queryset().count()
        live_aids_local_count = search_page.get_base_queryset().local_aids().count()
        return f'{live_aids_count} (dont aides locales : {live_aids_local_count})'
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


class SearchPageLiteAdmin(AdminLiteMixin, SearchPageAdmin):
    prepopulated_fields = {}
    fieldsets_with_inlines = LITE_FIELDSETS_SEARCH_PAGE


class MinisitePageAdmin(PageAdmin):
    list_display = ['url', 'title', 'minisite']
    list_filter = ['minisite']

    autocomplete_fields = ['minisite']

    list_display = ['url', 'title', 'minisite', 'date_created', 'date_updated']

    autocomplete_fields = ['minisite']
    readonly_fields = ['date_created', 'date_updated']
    fieldsets = (
        (None, {
            'fields': (
                'url',
                'minisite',
                'title',
                'content'
            )
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description'
            )
        }),
        ('Données diverses', {
            'fields': (
                'date_created',
                'date_updated'
            )
        })
    )

    def get_queryset(self, request):
        qs = MinisitePage.objects \
            .minisite_pages(for_user=request.user) \
            .select_related('minisite')
        return qs

    def get_list_filter(self, request):
        list_filter = self.list_filter

        if request.user.is_superuser:
            return list_filter

        return []


admin.site.register(SearchPage, SearchPageAdmin)
admin.site.register(MinisitePage, MinisitePageAdmin)
admin.site.register(SearchPageLite, SearchPageLiteAdmin)
