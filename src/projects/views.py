from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect

from projects.forms import ProjectCreateForm
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
        return context


class ProjectDeleteView(ContributorAndProfileCompleteRequiredMixin, DeleteView):
    """delete an existing project."""

    def get_queryset(self):
        queryset = Project.objects \
            .prefetch_related('aid_set')
        return queryset

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        confirmed = self.request.POST.get('confirm', False)
        if confirmed:
            self.object.delete()
            msg = 'Votre projet a été supprimé.'
            messages.success(self.request, msg)

        success_url = reverse('project_list_view')
        redirect = HttpResponseRedirect(success_url)
        return redirect
