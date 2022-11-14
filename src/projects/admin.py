from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse

from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats

from core.forms import RichTextField
from projects.models import Project
from projects.resources import ProjectResource


class ProjectForm(forms.ModelForm):
    description = RichTextField(label=_("Description"), required=False)

    class Meta:
        model = Project
        fields = "__all__"


class ProjectAdmin(ImportExportActionModelAdmin):

    resource_class = ProjectResource
    formats = [base_formats.CSV, base_formats.XLSX]
    form = ProjectForm
    list_display = ["name", "date_created", "is_public", "status"]
    list_filter = ["is_public", "status", "contract_link"]
    prepopulated_fields = {"slug": ("name",)}
    fields = [
        "name",
        "slug",
        "description",
        "private_description",
        "step",
        "budget",
        "key_words",
        "author",
        "organizations",
        "nb_aids_associated",
        "display_related_aids",
        "is_public",
        "contract_link",
        "project_types",
        "project_types_suggestion",
        "status",
        "date_created",
    ]
    search_fields = ["name"]
    readonly_fields = ["date_created", "nb_aids_associated", "display_related_aids"]
    autocomplete_fields = ["organizations", "author", "project_types"]

    def view_on_site(self, obj):
        url = reverse('public_project_detail_view', kwargs={'pk': obj.pk, 'slug': obj.slug})
        return url

    def display_related_aids(self, obj):
        related_aid_html = format_html(
            "<table> \
            <thead><tr> \
            <th>Aide</th> \
            </tr></thead> \
            <tbody>"
        )
        for aid in obj.aid_set.all():
            url = reverse("admin:aids_aid_change", args=(aid.pk,))
            related_aid_html += format_html(
                '<tr><td><a href="{url}">{name} (ID : {id})</a></td> \
                </tr>',
                url=url,
                name=aid.name,
                id=aid.pk,
            )
        related_aid_html += format_html("</tbody></table>")
        return related_aid_html

    display_related_aids.short_description = "Aides associées"

    def nb_aids_associated(self, obj):
        return obj.aid_set.count()

    nb_aids_associated.short_description = "Nombre d'aides associées"

    class Media:
        css = {
            "all": (
                "css/admin.css",
                "/static/trumbowyg/dist/ui/trumbowyg.css",
            )
        }
        js = [
            "admin/js/jquery.init.js",
            "/static/js/shared_config.js",
            "/static/js/plugins/softmaxlength.js",
            "/static/js/search/enable_softmaxlength.js",
            "/static/trumbowyg/dist/trumbowyg.js",
            "/static/trumbowyg/dist/langs/fr.js",
            "/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js",
            "/static/jquery-resizable-dom/dist/jquery-resizable.js",
            "/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js",
            "/static/js/enable_rich_text_editor.js",
        ]


admin.site.register(Project, ProjectAdmin)
