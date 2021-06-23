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


class MinisiteTab(Page):
    """
    Proxy class to make Page model available for minisites
    as a Tab.
    """
    class Meta:
        proxy = True
        verbose_name = "onglet (toutes les PP)"
        verbose_name_plural = "onglets (toutes les PP)"


class MinisiteTabLite(Page):
    """
    Proxy class to make a lite admin for ministe Tab.
    """
    class Meta:
        proxy = True
        verbose_name = "onglet"
        verbose_name_plural = "onglets"


class MinisiteTabInline(admin.TabularInline):
    model = MinisiteTab
    form = PageForm  # to display 'content' as RichTextField
    fields = ['url', 'title', 'content']
    extra = 1


class MinisiteTabLiteInline(MinisiteTabInline):
    """
    A lite version that's suitable for non superuser.
    """
    model = MinisiteTabLite


BASE_FIELDSETS_MINISITE_TAB = [
    (None, {
        'fields': (
            'url',
            'minisite',
            'title',
            'content'
        )
    }),
    ('À propos de cet onglet', {
        'fields': (
            'date_created',
            'date_updated'
        )
    }),
]

LITE_FIELDSETS_MINISITE_TAB = BASE_FIELDSETS_MINISITE_TAB.copy()

SUPERUSER_FIELDSETS_MINISITE_TAB = BASE_FIELDSETS_MINISITE_TAB.copy()
SUPERUSER_FIELDSETS_MINISITE_TAB.extend([
    ('SEO', {
        'fields': (
            'meta_title',
            'meta_description'
        )
    }),
])

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
LITE_FIELDSETS_SEARCH_PAGE.append(MinisiteTabLiteInline)

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
SUPERUSER_FIELDSETS_SEARCH_PAGE.extend([
    ('SEO', {
        'fields': (
            'meta_title',
            'meta_description',
            'meta_image',
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
])
SUPERUSER_FIELDSETS_SEARCH_PAGE.append(MinisiteTabInline)


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


class MinisiteTabAdmin(PageAdmin):
    list_display = ['url', 'title', 'minisite', 'date_created', 'date_updated']
    list_filter = ['minisite']
    autocomplete_fields = ['minisite']
    readonly_fields = ['date_created', 'date_updated']
    fieldsets = SUPERUSER_FIELDSETS_MINISITE_TAB

    def get_queryset(self, request):
        qs = MinisiteTab.objects \
            .minisite_tabs(for_user=request.user) \
            .select_related('minisite')
        return qs


class MinisiteTabLiteAdmin(AdminLiteMixin, MinisiteTabAdmin):
    list_display = ['url', 'title', 'date_created', 'date_updated']
    list_filter = []
    fieldsets = LITE_FIELDSETS_MINISITE_TAB


admin.site.register(SearchPage, SearchPageAdmin)
admin.site.register(MinisiteTab, MinisiteTabAdmin)
admin.site.register(SearchPageLite, SearchPageLiteAdmin)
