from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect

from projects.forms import ProjectCreateForm, ProjectMatchAidForm
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


class ProjectMatchAidView(ContributorAndProfileCompleteRequiredMixin, UpdateView):
    """Associate aid to an existing project."""

    template_name = 'projects/_match_aid_modal.html'
    form_class = ProjectMatchAidForm
    context_object_name = 'project'
    model = Project

    def form_valid(self, form):

        project = form.save(commit=False)
        project.save()

        '''
        Here we need to use some trick to add the new aid associated to the project
        without deleting the previous aids already associated to the project
        because form.save_m2m() is overwriting the M2M field
        So, we save in a list the id of all the previous aid associated
        Then, we save the new aid as M2M with form.save_M2M
        And we looping on the list off previous aids to re-add them
        '''
        project_aids = []
        for aid in self.object.aids_associated.all():
            project_aids.append(aid.id)

        form.save_m2m()
        for aid in project.aids_associated.all():
            new_aid_associated_slug = aid.slug

        for aid in project_aids:
            project.aids_associated.add(aid)

        msg = "L'aide a bien été associée à votre projet."
        messages.success(self.request, msg)
        url = reverse('aid_detail_view', args=[new_aid_associated_slug])
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
            .prefetch_related('aids_associated')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectDeleteView(ContributorAndProfileCompleteRequiredMixin, DeleteView):
    """delete an existing project."""

    def get_queryset(self):
        queryset = Project.objects \
            .prefetch_related('aids_associated')
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
