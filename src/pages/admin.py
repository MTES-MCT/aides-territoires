from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

from pages.models import Page


HELP = _("Note: it's not possible to change url of pages in the main menu.")


class PageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'content'),
            'description': '<div class="help">{}</div>'.format(HELP)}),
        (_('SEO'), {'fields': (
            'meta_title', 'meta_description')})
    )


admin.site.unregister(FlatPage)
admin.site.register(Page, PageAdmin)
