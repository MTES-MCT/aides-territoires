import operator
from itertools import groupby

from django import forms
from django.contrib import admin
from django.urls import reverse
from django.db.models import Count, Q
from django.utils.html import format_html

from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats

from core.forms import RichTextField
from core.constants import YES_NO_CHOICES
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS
from backers.models import BackerGroup, Backer
from backers.resources import BackerResource
from categories.models import Category
from programs.models import Program


class BackerGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'nb_backers', 'date_created']
    search_fields = ['id', 'name']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['date_created']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(backer_count=Count('backers'))
        return qs

    def nb_backers(self, backer_group):
        return backer_group.backer_count
    nb_backers.short_description = 'Nombre de porteurs'
    nb_backers.admin_order_field = 'backer_count'


class LogoFilter(admin.SimpleListFilter):
    """Custom admin filter to target backers with logos."""

    title = 'Logo du porteur'
    parameter_name = 'logo_status'

    def lookups(self, request, model_admin):
        return YES_NO_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.has_logo()
        elif value == 'No':
            return queryset.filter(Q(logo='') | Q(logo=None))
        return queryset


class BackerForm(forms.ModelForm):
    description = RichTextField(label='Description', required=False)

    class Meta:
        model = Backer
        fields = '__all__'


class BackerAdmin(ImportExportActionModelAdmin):
    """Admin module for aid backers."""

    resource_class = BackerResource
    formats = [base_formats.CSV, base_formats.XLSX]
    list_display = [
        'name', 'slug', 'group',
        'is_corporate', 'is_spotlighted', 'logo_status', 'perimeter',
        'nb_financed_aids', 'nb_instructed_aids',
        'date_created']
    list_filter = ['is_corporate', 'is_spotlighted', LogoFilter, 'group']
    list_editable = ['is_corporate', 'is_spotlighted']
    search_fields = ['name']
    ordering = ['name']

    form = BackerForm
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['perimeter']
    readonly_fields = [
        'nb_financed_aids', 'nb_instructed_aids', 'display_related_aids',
        'display_related_themes', 'display_related_programs',
        'date_created']

    fieldsets = [
        ('', {
            'fields': (
                'name',
                'slug',
                'description',
                'logo',
                'external_link',
                'perimeter',
                'is_corporate',
                'is_spotlighted',
            )
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
            )
        }),
        ('Groupe de porteurs', {
            'fields': (
                'group',
            )
        }),
        ('Données diverses', {
            'fields': (
                'nb_financed_aids',
                'nb_instructed_aids',
                'display_related_aids',
                'display_related_themes',
                'display_related_programs',
                'date_created',
            )
        }),
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs \
            .annotate_aids_count(Backer.financed_aids, 'nb_financed_aids') \
            .annotate_aids_count(Backer.instructed_aids, 'nb_instructed_aids')
        return qs

    def nb_financed_aids(self, obj):
        return obj.nb_financed_aids
    nb_financed_aids.short_description = 'Aides financées'
    nb_financed_aids.admin_order_field = 'nb_financed_aids'

    def nb_instructed_aids(self, obj):
        return obj.nb_instructed_aids
    nb_instructed_aids.short_description = 'Aides instruites'
    nb_instructed_aids.admin_order_field = 'nb_instructed_aids'

    def logo_status(self, backer):
        return backer.has_logo()
    logo_status.boolean = True
    logo_status.short_description = 'Logo du porteur'

    def display_related_aids(self, obj):
        related_aid_html = format_html('<table> \
            <thead><tr> \
            <th>Auteur</th> \
            <th>Aide</th> \
            </tr></thead> \
            <tbody>')
        for aid in obj.financed_aids.all().order_by('name') \
                .select_related('author'):
            url = reverse("admin:aids_aid_change", args=(aid.pk,))
            related_aid_html += format_html(
                '<tr><td>{author}</td> \
                    <td><a href="{url}">{name} (ID : {id})</a></td> \
                </tr>',
                url=url,
                name=aid.name,
                id=aid.pk,
                author=aid.author
            )
        related_aid_html += format_html('</tbody></table>')
        return related_aid_html
    display_related_aids.short_description = 'Aides associées'

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
    display_related_themes.short_description = 'Thématiques associées'

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
    display_related_programs.short_description = 'Programmes associés'

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
            '/static/jquery-resizable-dom/dist/jquery-resizable.js',
            '/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js',
            '/static/js/enable_rich_text_editor.js',
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS


admin.site.register(BackerGroup, BackerGroupAdmin)
admin.site.register(Backer, BackerAdmin)
