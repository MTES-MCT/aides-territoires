from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

from core.forms import RichTextField
from pages.models import Page
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class PageForm(FlatpageForm):
    content = RichTextField(label=_('Content'))

    class Meta:
        model = Page
        fields = '__all__'


class PageAdmin(FlatPageAdmin):

    HELP = _("WARNING! DON'T CHANGE url of pages in the main menu.")

    list_display = ['url', 'title', 'date_created', 'date_updated']

    form = PageForm
    readonly_fields = ['date_created', 'date_updated']
    fieldsets = (
        (None, {
            'description': '<div class="help">{}</div>'.format(HELP),
            'fields': (
                'url',
                'title',
                'content'
            )
        }),
        (_('SEO'), {
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
        qs = super().get_queryset(request).at_pages()
        return qs

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
            '/static/trumbowyg/dist/trumbowyg.js',
            '/static/trumbowyg/dist/langs/fr.js',
            '/static/js/enable_rich_text_editor.js',
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS


admin.site.unregister(FlatPage)
admin.site.register(Page, PageAdmin)
