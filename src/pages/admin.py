from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage

from django.core.exceptions import ValidationError


from core.forms import RichTextField
from pages.models import Page
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class PageForm(FlatpageForm):
    content = RichTextField(label="Contenu")

    class Meta:
        model = Page
        fields = "__all__"

    def clean(self):
        url = self.cleaned_data.get("url")

        same_url = FlatPage.objects.filter(url=url)
        if self.instance.pk:
            same_url = same_url.exclude(pk=self.instance.pk)

        if same_url.exists():
            raise ValidationError(
                "L'url %(url)s existe déjà sur le site Aides-territoires. Veuillez choisir une url davantage personnalisée.",  # noqa
                code="duplicate_url",
                params={"url": url},
            )

        return super().clean()


class PageAdmin(FlatPageAdmin):
    list_display = ["url", "title", "date_created", "date_updated"]

    form = PageForm
    readonly_fields = ["date_created", "date_updated"]
    HELP = "ATTENTION ! NE PAS CHANGER l'url des pages du menu principal."

    fieldsets = (
        (
            None,
            {
                "description": '<div class="help">{}</div>'.format(HELP),
                "fields": ("url", "title", "content"),
            },
        ),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request).at_pages(for_user=request.user)
        return qs

    class Media:
        css = {
            "all": (
                "/static/css/admin.css",
                "/static/trumbowyg/dist/ui/trumbowyg.css",
            )
        }
        js = [
            "admin/js/jquery.init.js",
            "/static/js/shared_config.js",
            "/static/trumbowyg/dist/trumbowyg.js",
            "/static/trumbowyg/dist/langs/fr.js",
            "/static/js/enable_rich_text_editor.js",
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS


admin.site.unregister(FlatPage)
admin.site.register(Page, PageAdmin)
