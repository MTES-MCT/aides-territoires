from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from braces.views import MessageMixin

from projects.forms import ProjectCreateForm, ProjectUpdateForm
from projects.models import Project
from aids.models import AidProject
from geofr.models import Perimeter
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
        project.author.add(self.request.user)
        project.organizations.add(self.request.user.beneficiary_organization)

        msg = 'Votre nouveau projet a été créé&nbsp;!'
        messages.success(self.request, msg)
        url = reverse('project_list_view')
        url = '{}'.format(url)
        return HttpResponseRedirect(url)


class ProjectListView(ContributorAndProfileCompleteRequiredMixin, ListView):
    """User Project Dashboard"""

    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'
    paginate_by = 18

    def get_queryset(self):
        if self.request.user.beneficiary_organization is not None:
            queryset = Project.objects \
                .filter(organizations=self.request.user.beneficiary_organization.pk) \
                .prefetch_related('aid_set')
        else:
            queryset = Project.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['project_create_form'] = ProjectCreateForm(label_suffix='')
        user_org = self.request.user.beneficiary_organization

        # if user's organization is a commune and if organization's perimeter is defined
        # we create a querystring with targeted_audience & perimeter
        # to allow user to make a research skipping step 1 and 2
        if user_org.organization_type[0] == 'commune' and user_org.zip_code:
            org_zip_code = str(user_org.zip_code).split()
            org_perimeter = Perimeter.objects.filter(zipcodes=org_zip_code).first()
            # here we check if zipcode is related to an existing perimeter
            if org_perimeter:
                org_perimeter = org_perimeter.id_slug
                context['user_querystring'] = 'targeted_audiences=commune' \
                    f'&perimeter={org_perimeter}&action=search'

        return context


class ProjectDetailView(ContributorAndProfileCompleteRequiredMixin, DetailView):
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        queryset = Project.objects \
            .prefetch_related('aid_set')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['aid_set'] = self.object.aid_set.all()
        context['AidProject'] = AidProject.objects.filter(project=self.object.pk)
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
        url = self.object.get_absolute_url()
        return '{}'.format(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object
        return context
