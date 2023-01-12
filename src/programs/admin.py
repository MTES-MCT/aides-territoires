from django import forms
from django.contrib import admin
from django.db.models import Count

from core.forms import RichTextField
from programs.models import Program, ProgramTab
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS

from pages.admin import TabAdmin


class ProgramAdminForm(forms.ModelForm):
    description = RichTextField(label="Description")


class ProgramAdmin(admin.ModelAdmin):

    list_display = ["name", "slug", "perimeter", "nb_aids", "date_created"]
    search_fields = ["name"]

    form = ProgramAdminForm
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["perimeter"]
    readonly_fields = ["nb_aids", "date_created"]

    fieldsets = [
        (
            "",
            {
                "fields": (
                    "name",
                    "slug",
                    "is_spotlighted",
                    "short_description",
                    "description",
                    "logo",
                    "perimeter",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                )
            },
        ),
        (
            "Données diverses",
            {
                "fields": (
                    "nb_aids",
                    "date_created",
                )
            },
        ),
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("aids").annotate(aid_count=Count("aids"))
        return qs

    def nb_aids(self, obj):
        return obj.aid_count

    nb_aids.short_description = "Nombre d'aides"
    nb_aids.admin_order_field = "aid_count"

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


class ProgramTabAdmin(TabAdmin):
    list_display = ["title", "program", "date_created", "date_updated"]
    list_filter = ["program"]
    autocomplete_fields = ["program"]
    readonly_fields = ["date_created", "date_updated"]
    fieldsets = [
        (
            None,
            {
                "fields": ("program", "title", "content"),
            },
        ),
        ("À propos de cet onglet", {"fields": ("date_created", "date_updated")}),
    ]


admin.site.register(Program, ProgramAdmin)
admin.site.register(ProgramTab, ProgramTabAdmin)
