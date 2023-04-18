from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse, path

from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats

from core.forms import RichTextField
from exporting.tasks import (
    export_projects_as_csv,
    export_projects_as_xlsx,
    export_validated_projects_as_csv,
    export_validated_projects_as_xlsx,
)
from exporting.utils import get_admin_export_message
from projects.models import Project, ValidatedProject
from projects.resources import ProjectResource
from projects.admin_views import ImportValidatedProjects


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
    list_filter = [
        "is_public",
        "status",
        "contract_link",
    ]
    prepopulated_fields = {"slug": ("name",)}
    fields = [
        "name",
        "slug",
        "description",
        "private_description",
        "image",
        "due_date",
        "step",
        "budget",
        "key_words",
        "author",
        "organizations",
        "other_project_owner",
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
    actions = ["export_csv", "export_xlsx"]

    def view_on_site(self, obj):
        url = reverse(
            "public_project_detail_view", kwargs={"pk": obj.pk, "slug": obj.slug}
        )
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

    nb_aids_associated.short_description = "Nombre d’aides associées"

    def show_export_message(self, request):
        self.message_user(request, get_admin_export_message())

    def export_csv(self, request, queryset):
        aids_id_list = list(queryset.values_list("id", flat=True))
        export_projects_as_csv.delay(aids_id_list, request.user.id)
        self.show_export_message(request)

    export_csv.short_description = (
        "Exporter les projets sélectionnés en CSV en tâche de fond"
    )

    def export_xlsx(self, request, queryset):
        aids_id_list = list(queryset.values_list("id", flat=True))
        export_projects_as_xlsx.delay(aids_id_list, request.user.id)
        self.show_export_message(request)

    export_xlsx.short_description = (
        "Exporter les projets sélectionnés en XLSX en tâche de fond"
    )

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


class ValidatedProjectAdmin(admin.ModelAdmin):
    change_list_template = "admin/projects/change_list_template.html"
    form = ProjectForm
    list_display = [
        "project_name",
        "aid_name",
        "organization",
        "financer_name",
        "date_obtained",
        "amount_obtained",
    ]

    fields = [
        "project_name",
        "project_linked",
        "description",
        "aid_name",
        "aid_linked",
        "organization",
        "financer_name",
        "financer_linked",
        "budget",
        "amount_obtained",
        "date_obtained",
        "date_created",
    ]
    readonly_fields = ["date_created"]
    autocomplete_fields = [
        "aid_linked",
        "project_linked",
        "financer_linked",
        "organization",
    ]
    search_fields = ["project_name"]
    actions = ["export_csv", "export_xlsx"]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "validated_projects_import/",
                self.admin_site.admin_view(self.validated_projects_import_view),
                name="validated_projects_import",
            ),
        ]
        return my_urls + urls

    def validated_projects_import_view(self, request, object_id=None):
        """Display the form to upload a list of validated projects."""

        opts = self.model._meta
        app_label = opts.app_label
        obj = self.get_object(request, object_id)

        context = {
            **self.admin_site.each_context(request),
            "title": "Import des projets subventionnés",
            "opts": opts,
            "app_label": app_label,
            "original": obj,
        }
        return ImportValidatedProjects.as_view(extra_context=context)(
            request, object_id=object_id
        )

    def show_export_message(self, request):
        self.message_user(request, get_admin_export_message())

    def export_csv(self, request, queryset):
        aids_id_list = list(queryset.values_list("id", flat=True))
        export_validated_projects_as_csv.delay(aids_id_list, request.user.id)
        self.show_export_message(request)

    export_csv.short_description = (
        "Exporter les projets subventionnés sélectionnés en CSV en tâche de fond"
    )

    def export_xlsx(self, request, queryset):
        aids_id_list = list(queryset.values_list("id", flat=True))
        export_validated_projects_as_xlsx.delay(aids_id_list, request.user.id)
        self.show_export_message(request)

    export_xlsx.short_description = (
        "Exporter les projets subventionnés sélectionnés en XLSX en tâche de fond"
    )

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


admin.site.register(ValidatedProject, ValidatedProjectAdmin)
admin.site.register(Project, ProjectAdmin)
