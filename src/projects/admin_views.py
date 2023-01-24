from django.views.generic import FormView
from django.urls import reverse_lazy
from braces.views import MessageMixin

from projects.models import ValidatedProject
from projects.forms import ValidatedProjectImportForm
from projects.services.import_validated_projects import import_validated_projects


class ImportValidatedProjects(MessageMixin, FormView):
    """Import validated projects in database from xlsx file."""

    template_name = "admin/import_validated_projects.html"
    form_class = ValidatedProjectImportForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_queryset(self):
        qs = ValidatedProject.objects.all()
        return qs

    def get_success_url(self):
        return reverse_lazy("admin:projects_validatedproject_changelist")

    def form_valid(self, form):
        import_validated_projects()
        msg = "Les projets subventionnés ont été importés avec succès."
        self.messages.success(msg)

        return super().form_valid(form)
