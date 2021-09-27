from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from braces.views import MessageMixin

from projects.forms import ProjectCreateForm, ProjectUpdateForm
from projects.models import Project
from django.contrib import messages
from accounts.mixins import ContributorAndProfileCompleteRequiredMixin


class ProjectCreateView(ContributorAndProfileCompleteRequiredMixin, CreateView):
    """Allows users to create their own projects."""

    template_name = 'projects/_create_project_modal.html'
    form_class = ProjectCreateForm
    context_object_name = 'project'

    def form_valid(self, form):

        project = form.save(commit=False)
        project.save()
        form.save_m2m()
        project.beneficiary.add(self.request.user)

        msg = 'Votre nouveau projet a été créé&nbsp;!'
        messages.success(self.request, msg)
        url = reverse('project_list_view')
        url = '{}'.format(url)
        return HttpResponseRedirect(url)


class ProjectListView(ListView):
    """User Project Dashboard"""

    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'
    paginate_by = 18

    def get_queryset(self):
        queryset = Project.objects \
            .filter(beneficiary=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_create_form'] = ProjectCreateForm(label_suffix='')

        return context


class ProjectDetailView(DetailView):
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        queryset = Project.objects \
            .prefetch_related('aid_set')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['project_update_form'] = ProjectUpdateForm(label_suffix='')
        return context


class ProjectDeleteView(ContributorAndProfileCompleteRequiredMixin, DeleteView):
    """Delete an existing project."""

    def get_queryset(self):
        qs = Project.objects.all()
        self.queryset = qs
        return super().get_queryset()

    def get_success_url(self):
        url = reverse('project_list_view')
        return url

    def delete(self, *args, **kwargs):
        res = super().delete(*args, **kwargs)
        msg = "Votre projet a été supprimé." # noqa
        messages.success(self.request, msg)
        return res


class ProjectUpdateView(ContributorAndProfileCompleteRequiredMixin, MessageMixin, UpdateView):
    """Edit an existing project."""

    template_name = 'projects/update_project.html'
    context_object_name = 'project'
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
        url = reverse('project_detail_view', args=[self.object.slug])
        return '{}'.format(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object
        return context

