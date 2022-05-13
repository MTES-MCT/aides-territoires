from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from braces.views import MessageMixin

from projects.tasks import send_project_deleted_email
from projects.forms import ProjectCreateForm, ProjectUpdateForm
from projects.models import Project
from aids.models import AidProject, Aid
from aids.views import AidPaginator
from aids.forms import AidSearchForm
from accounts.mixins import ContributorAndProfileCompleteRequiredMixin


class ProjectCreateView(ContributorAndProfileCompleteRequiredMixin, CreateView):
    """Allows users to create their own projects."""

    template_name = "projects/_create_project_modal.html"
    form_class = ProjectCreateForm
    context_object_name = "project"

    def form_valid(self, form):

        project = form.save(commit=False)
        project.save()
        form.save_m2m()
        project.author.add(self.request.user)
        project.organizations.add(self.request.user.beneficiary_organization)

        msg = "Votre nouveau projet a été créé&nbsp;!"
        messages.success(self.request, msg)
        url = reverse("project_list_view")
        project = f"project_created={project.pk}"
        url = f"{url}?{project}"
        return HttpResponseRedirect(url)


class ProjectListView(ContributorAndProfileCompleteRequiredMixin, ListView):
    """User Project Dashboard"""

    template_name = "projects/projects_list.html"
    context_object_name = "projects"
    paginate_by = 18
    paginator_class = AidPaginator

    def get_queryset(self):
        if self.request.user.beneficiary_organization is not None:
            queryset = Project.objects.filter(
                organizations=self.request.user.beneficiary_organization.pk
            )
        else:
            queryset = Project.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["project_create_form"] = ProjectCreateForm(label_suffix="")

        # Here we add some data for the project_search_aid modal
        if "project_created" in self.request.GET:
            context["project_created"] = self.request.GET["project_created"]
            project_created = Project.objects.get(
                pk=self.request.GET["project_created"]
            )
            text = project_created.name.split(" ")
            text_encoded = "+".join(text)
            if self.request.user.beneficiary_organization.perimeter:
                perimeter = self.request.user.beneficiary_organization.perimeter.pk
            else:
                perimeter = ""
            audience_list = self.request.user.beneficiary_organization.organization_type
            audience = audience_list[0]
            aids = Aid.objects.live()
            form = AidSearchForm(
                {
                    "text": text_encoded,
                    "targeted_audiences": audience_list,
                    "perimeter": perimeter,
                }
            )
            qs = form.filter_queryset(aids)
            aid_results = qs.count()
            context["aid_results"] = aid_results
            context["perimeter"] = perimeter
            context["audience"] = audience
            context["text_encoded"] = text_encoded
        return context


class ProjectDetailView(ContributorAndProfileCompleteRequiredMixin, DetailView):
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        queryset = Project.objects.prefetch_related("aid_set")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["aid_set"] = self.object.aid_set.all()
        context["AidProject"] = AidProject.objects.filter(project=self.object.pk)
        context["project_update_form"] = ProjectUpdateForm(label_suffix="")
        return context


class ProjectDeleteView(ContributorAndProfileCompleteRequiredMixin, DeleteView):
    """Delete an existing project."""

    def get_queryset(self):
        qs = Project.objects.all()
        self.queryset = qs
        return super().get_queryset()

    def get_success_url(self):
        url = reverse("project_list_view")
        return url

    def delete(self, *args, **kwargs):
        project_name = self.get_object().name
        eraser = self.request.user
        eraser_email = self.request.user.email
        eraser_name = self.request.user.full_name
        res = super().delete(*args, **kwargs)
        for user in eraser.beneficiary_organization.beneficiaries.all():
            user_email = user.email
            if user_email != eraser_email:
                send_project_deleted_email.delay(user_email, project_name, eraser_name)
        msg = f"Votre projet { project_name } a bien été supprimé."  # noqa
        messages.success(self.request, msg)
        return res


class ProjectUpdateView(
    ContributorAndProfileCompleteRequiredMixin, MessageMixin, UpdateView
):
    """Edit an existing project."""

    template_name = "projects/update_project.html"
    context_object_name = "project"
    form_class = ProjectUpdateForm

    def get_queryset(self):
        qs = Project.objects.all()
        self.queryset = qs
        return super().get_queryset()

    def form_valid(self, form):

        response = super().form_valid(form)

        msg = "Le projet a bien été mis à jour."

        self.messages.success(msg)
        return response

    def get_success_url(self):
        url = self.object.get_absolute_url()
        return "{}".format(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.object
        return context
