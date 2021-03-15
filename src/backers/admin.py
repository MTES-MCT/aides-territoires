import operator
from itertools import groupby

from django import forms
from django.contrib import admin
from django.urls import reverse
from django.db.models import Count, Q
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from import_export import resources
from import_export.admin import ImportMixin
from import_export.formats import base_formats

from core.forms import RichTextField
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS
from backers.models import BackerGroup, Backer
from categories.models import Category
from programs.models import Program


class BackerGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'nb_backers', 'date_created']
    search_fields = ['name']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['date_created']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(backer_count=Count('backers'))
        return qs

    def nb_backers(self, backer_group):
        return backer_group.backer_count
    nb_backers.short_description = _('Number of backers')
    nb_backers.admin_order_field = 'backer_count'


class LogoFilter(admin.SimpleListFilter):
    """Custom admin filter to target backers with logos."""

    title = _('Logo image')
    parameter_name = 'logo_status'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.has_logo()
        elif value == 'No':
            return queryset.filter(Q(logo='') | Q(logo=None))
        return queryset


class BackerResource(resources.ModelResource):
    """Resource for Import-export."""

    class Meta:
        model = Backer
        skip_unchanged = True
        # name must be unique
        import_id_fields = ('name',)
        fields = ('name',)


class BackerForm(forms.ModelForm):
    description = RichTextField(label=_('Description'), required=False)

    class Meta:
        model = Backer
        fields = '__all__'


class BackerAdmin(ImportMixin, admin.ModelAdmin):
    """Admin module for aid backers."""

    resource_class = BackerResource
    form = BackerForm
    formats = [base_formats.CSV, base_formats.XLSX]
    list_display = ['name', 'slug', 'group',
                    'is_corporate', 'is_spotlighted', 'logo_status',
                    'nb_financed_aids', 'nb_instructed_aids',
                    'date_created']
    list_filter = ['is_corporate', 'is_spotlighted', LogoFilter, 'group']
    list_editable = ['is_corporate', 'is_spotlighted']
    search_fields = ['name']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['date_created', 'display_related_aids',
                       'display_related_themes', 'display_related_programs']

    fieldsets = [
        ('', {
            'fields': (
                'name',
                'slug',
                'description',
                'logo',
                'external_link',
                'is_corporate',
                'is_spotlighted',
                'date_created',
                'display_related_aids',
                'display_related_themes',
                'display_related_programs'
            )
        }),
        (_('SEO'), {
            'fields': (
                'meta_title',
                'meta_description',
            )
        }),
        (_('Backer Group'), {
            'fields': (
                'group',
            )
        })
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs \
            .annotate_aids_count(Backer.financed_aids, 'nb_financed_aids') \
            .annotate_aids_count(Backer.instructed_aids, 'nb_instructed_aids')
        return qs

    def nb_financed_aids(self, obj):
        return obj.nb_financed_aids
    nb_financed_aids.short_description = _('Financed aids')
    nb_financed_aids.admin_order_field = 'nb_financed_aids'

    def nb_instructed_aids(self, obj):
        return obj.nb_instructed_aids
    nb_instructed_aids.short_description = _('Instructed aids')
    nb_instructed_aids.admin_order_field = 'nb_instructed_aids'

    def logo_status(self, backer):
        return backer.has_logo()
    logo_status.boolean = True
    logo_status.short_description = _('Logo image')

    def display_related_aids(self, obj):
        related_aid_html = format_html('<div>')
        for aid in obj.financed_aids.all().order_by('name'):
            url = reverse("admin:aids_aid_change", args=(aid.pk,))
            related_aid_html += format_html(
                '<p>auteur : {author} <a href="{url}">{name} (ID : {id})</a></p>',
                url=url,
                name=aid.name,
                id=aid.pk,
                author=aid.author
            )
        related_aid_html += format_html('</div>')
        return related_aid_html
    display_related_aids.short_description = _('Related aids')

    def display_related_themes(self, obj):
        """Display the related themes."""

        categories = Category.objects \
            .select_related('theme') \
            .order_by('theme__name', 'name') \
            .filter(Q(aids__financers=obj) | Q(aids__instructors=obj)) \
            .values_list('theme__name', 'name') \
            .distinct()

        themes = groupby(categories, operator.itemgetter(0))

        related_themes_html = format_html('<ul>')
        for theme, theme_categories in themes:
            related_themes_html += format_html(
                '<li><strong>{theme} > </strong>',
                theme=theme)
            for k, theme_category in theme_categories:
                related_themes_html += format_html(
                    '{category}. ',
                    category=theme_category)
            related_themes_html += format_html('<li>')
        related_themes_html += format_html('</ul>')
        return related_themes_html
    display_related_themes.short_description = _('Related themes')

    def display_related_programs(self, obj):
        """Display the related programs."""

        programs = Program.objects \
            .filter(aids__in=obj.financed_aids.all()) \
            .distinct()

        related_programs_html = format_html('<ul>')
        for program in programs:
            related_programs_html += format_html(
                '<li><strong>{program_name}</strong></li>',
                program_name=program.name
            )
        related_programs_html += format_html('</ul>')
        return related_programs_html
    display_related_programs.short_description = _('Related programs')

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


admin.site.register(BackerGroup, BackerGroupAdmin)
admin.site.register(Backer, BackerAdmin)
