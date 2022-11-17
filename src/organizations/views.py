from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied


from accounts.mixins import ContributorAndProfileCompleteRequiredMixin

from organizations.forms import (
    OrganizationCreateForm,
    OrganizationUpdateForm,
    ProjectToFavoriteForm,
)
from accounts.models import User
from organizations.models import Organization
from projects.models import Project


class OrganizationCreateView(CreateView):

    template_name = "organizations/create.html"
    form_class = OrganizationCreateForm
    context_object_name = "organization"

    def form_valid(self, form):

        if self.request.user.email:
            user_email = self.request.user.email
            user_organization_type = self.request.POST.get("organization_type")
        else:
            return

        organization = form.save(commit=False)
        organization.organization_type = [user_organization_type]
        if organization.perimeter.zipcodes is not None:
            organization.zip_code = organization.perimeter.zipcodes[0]
            organization.city_name = organization.perimeter.name
        organization.save()
        form.save_m2m()

        user_id = User.objects.filter(email=user_email).first().pk
        organization.beneficiaries.add(user_id)
        User.objects.filter(pk=user_id).update(beneficiary_organization=organization.pk)

        if self.request.user.email:
            msg = "Votre profil a bien été mis à jour !"
            messages.success(self.request, msg)
            success_url = reverse("user_dashboard")

        return HttpResponseRedirect(success_url)


class OrganizationUpdateView(ContributorAndProfileCompleteRequiredMixin, UpdateView):

    template_name = "organizations/update.html"
    form_class = OrganizationUpdateForm
    context_object_name = "organization"

    def get_object(self, queryset=None):
        """
        Require `self.queryset` and a `pk` argument in the URLconf.
        Require also user in the organization object
        """
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        user = self.request.user
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
            if user not in obj.beneficiaries.all():
                raise PermissionDenied()
        except queryset.model.DoesNotExist:
            raise Http404()
        return obj

    def form_valid(self, form):

        organization = form.save(commit=False)
        organization.save()

        msg = "Les informations de votre structure ont bien été mises à jour."
        messages.success(self.request, msg)
        success_url = reverse("organization_update_view", args=[self.object.pk])
        return HttpResponseRedirect(success_url)

    def get_queryset(self):
        qs = Organization.objects.all()
        self.queryset = qs
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organization"] = self.object
        return context


class AddProjectToFavoriteView(ContributorAndProfileCompleteRequiredMixin, UpdateView):
    """Add project to favorite-projects-list of the organization."""

    template_name = "projects/_add_to_favorite_modal.html"
    form_class = ProjectToFavoriteForm
    context_object_name = "organization"
    model = Organization

    def form_valid(self, form):

        organization = form.save(commit=False)

        if self.request.POST.get("favorite_projects"):
            # add the project to the favorite_projects_list
            project_pk = self.request.POST.get("favorite_projects")

            try:
                project = Project.objects.get(pk=project_pk)
                if (
                    project.is_public is False
                    or project.status != Project.STATUS.published
                ):
                    raise PermissionDenied()
                else:
                    organization.favorite_projects.add(project_pk)
                    organization.save()
            except Exception:
                raise PermissionDenied()

            # retrieve project's data to create successful message
            project_obj = Project.objects.get(pk=project_pk)
            project_name = project_obj.name
            project_slug = project_obj.slug
            favorite_projects_url = reverse("favorite_project_list_view")
            msg = (f"Le projet «{project_name}» a bien été ajouté à \
                <a href='{favorite_projects_url}'>vos projets favoris<a/>.")
            messages.success(self.request, msg)

        url = reverse("public_project_detail_view", args=[project_pk, project_slug])
        return HttpResponseRedirect(url)


class RemoveProjectFromFavoriteView(ContributorAndProfileCompleteRequiredMixin, UpdateView):
    """Remove project from favorite-projects-list of the organization."""

    template_name = "projects/_remove_from_favorite_modal.html"
    form_class = ProjectToFavoriteForm
    context_object_name = "organization"
    model = Organization

    def form_valid(self, form):

        organization = form.save(commit=False)

        if self.request.POST.get("favorite_projects"):
            # remove the project from the favorite_projects_list
            project_pk = self.request.POST.get("favorite_projects")

            try:
                if self.request.user.beneficiary_organization == organization:
                    organization.favorite_projects.remove(project_pk)
                    organization.save()
                else:
                    raise PermissionDenied()
            except Exception:
                raise PermissionDenied()

            # retrieve project's data to create successful message
            project_obj = Project.objects.get(pk=project_pk)
            project_name = project_obj.name
            project_slug = project_obj.slug
            favorite_projects_url = reverse("favorite_project_list_view")
            msg = (f"Le projet «{project_name}» a bien été retiré de \
                <a href='{favorite_projects_url}'>vos projets favoris<a/>.")
            messages.success(self.request, msg)

        if self.request.POST.get("origin_page"):
            url = reverse("favorite_project_list_view")
        else:
            url = reverse("public_project_detail_view", args=[project_pk, project_slug])
        return HttpResponseRedirect(url)
