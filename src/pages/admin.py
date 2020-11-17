from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

from core.forms import RichTextField
from pages.models import Page


class PageForm(FlatpageForm):
    content = RichTextField(label=_('Content'))

    class Meta:
        model = Page
        fields = '__all__'


class PageAdmin(FlatPageAdmin):

    HELP = _("WARNING! DON'T CHANGE url of pages in the main menu.")

    class Media:
        css = {
            'all': (
                '/static/css/admin.css',
                '/static/trumbowyg/dist/ui/trumbowyg.css',
            )
        }
        js = [
            'admin/js/jquery.init.js',
            '/static/trumbowyg/dist/trumbowyg.js',
            '/static/trumbowyg/dist/langs/fr.js',
            '/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js',
            '/static/trumbowyg/dist/plugins/resizimg/resizable-resolveconflict.js',  # noqa
            '/static/jquery-resizable-dom/dist/jquery-resizable.js',
            '/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js',
            '/static/js/enable_rich_text_editor.js',
        ]

    form = PageForm
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'content'),
            'description': '<div class="help">{}</div>'.format(HELP)}),
        (_('SEO'), {'fields': (
            'meta_title', 'meta_description')})
    )


admin.site.unregister(FlatPage)
admin.site.register(Page, PageAdmin)
