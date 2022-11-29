from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.views.generic.edit import FormMixin
from django.db.models import Prefetch

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from braces.views import MessageMixin
from projects.constants import EXPORT_FORMAT_KEYS
from projects.services.export import export_project

from projects.tasks import send_project_deleted_email
from projects.forms import (
    ProjectCreateForm,
    ProjectExportForm,
    ProjectUpdateForm,
    ProjectSearchForm,
)
from projects.models import Project
from organizations.models import Organization
from aids.models import AidProject, Aid, SuggestedAidProject
from aids.views import AidPaginator
from aids.forms import AidSearchForm, SuggestAidMatchProjectForm, AidProjectStatusForm
from accounts.mixins import ContributorAndProfileCompleteRequiredMixin
from minisites.mixins import SearchMixin


class ProjectCreateView(ContributorAndProfileCompleteRequiredMixin, CreateView):
    """Allows users to create their own projects."""

    template_name = "projects/create_project.html"
    form_class = ProjectCreateForm
    context_object_name = "project"

    def form_valid(self, form):
        form = ProjectCreateForm(self.request.POST, self.request.FILES)
        project = form.save(commit=False)
        if project.is_public is True:
            project.status = Project.STATUS.reviewable
        else:
            project.status = Project.STATUS.draft
        if self.request.FILES:
            project.image = self.request.FILES["image"]
        project.save()
        form.save_m2m()
        project.author.add(self.request.user)
        project.organizations.add(self.request.user.beneficiary_organization)

        msg = "Votre nouveau projet a été créé !"
        messages.success(self.request, msg)
        url = reverse("project_list_view")
        project = f"project_created={project.pk}"
        url = f"{url}?{project}"
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org_type = self.request.user.beneficiary_organization.organization_type[0]
        org_details = self.request.user.beneficiary_organization.details_completed()
        if org_type == "commune" or org_type == "epci":
            context["org_is_commune_or_epci"] = True
            if org_details:
                context["org_details_completed"] = True
        return context


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
        org_type = self.request.user.beneficiary_organization.organization_type[0]
        if org_type == "commune" or org_type == "epci":
            context["org_is_commune_or_epci"] = True

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


class FavoriteProjectListView(ContributorAndProfileCompleteRequiredMixin, ListView):
    """User Favorite Projects Dashboard"""

    template_name = "projects/favorite_projects_list.html"
    context_object_name = "projects"
    paginate_by = 18
    paginator_class = AidPaginator

    def get_queryset(self):
        if self.request.user.beneficiary_organization is not None:
            queryset = Project.objects.filter(
                organization_favorite=self.request.user.beneficiary_organization,
                is_public=True,
                status=Project.STATUS.published,
            )
        else:
            queryset = Project.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class PublicProjectListView(SearchMixin, FormMixin, ListView):
    """Search and display public projects."""

    template_name = "projects/public_projects_list.html"
    context_object_name = "projects"
    form_class = ProjectSearchForm
    paginate_by = 18
    paginator_class = AidPaginator

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.form.full_clean()
        self.store_current_search()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Return the list of results to display."""

        organizations_qs = Organization.objects.all().select_related("perimeter")

        qs = (
            Project.objects.filter(is_public=True, status=Project.STATUS.published)
            .prefetch_related(Prefetch("organizations", queryset=organizations_qs))
            .prefetch_related("project_types")
            .prefetch_related("aid_set")
        )

        filter_form = self.form
        results = filter_form.filter_queryset(qs).distinct()

        return results

    def store_current_search(self):
        """Store the current search query in a cookie.

        This is needed to provide the correct "go back to your search" link in
        other pages' breadcrumbs.
        """
        current_search_query = self.request.GET.urlencode()
        self.request.session[settings.SEARCH_COOKIE_NAME] = current_search_query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["current_search"] = self.request.session.get(
            settings.SEARCH_COOKIE_NAME, ""
        )
        context["user"] = self.request.user
        if self.request.user.is_authenticated:
            if self.request.user.beneficiary_organization:
                context["user_has_organization"] = True
                context[
                    "user_favorite_projects"
                ] = self.request.user.beneficiary_organization.favorite_projects.all()
        return context


class ProjectDetailView(ContributorAndProfileCompleteRequiredMixin, DetailView):
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_object(self, queryset=None):
        """
        Require `self.queryset` and a `pk` AND `slug` argument in the URLconf.
        """
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        user = self.request.user
        if pk is not None and slug is not None:
            queryset = queryset.filter(pk=pk, slug=slug)

        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
            if user not in obj.organizations.first().beneficiaries.all():
                raise PermissionDenied()
        except queryset.model.DoesNotExist:
            raise Http404()
        return obj

    def get_queryset(self):
        queryset = Project.objects.prefetch_related("aid_set")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["aid_set"] = self.object.aid_set.all()
        context["AidProject"] = AidProject.objects.filter(project=self.object.pk)
        context["SuggestedAidProject"] = SuggestedAidProject.objects.filter(
            project=self.object.pk
        )
        context["suggested_aid"] = self.object.suggested_aid.filter(
            suggestedaidproject__is_associated=False,
            suggestedaidproject__is_rejected=False,
        )
        context["aid_project_status_form"] = AidProjectStatusForm
        context["project_update_form"] = ProjectUpdateForm(label_suffix="")
        context["form"] = ProjectExportForm
        return context


class PublicProjectDetailView(DetailView):
    template_name = "projects/public_project_detail.html"
    context_object_name = "project"

    def get_object(self, queryset=None):
        """
        Require `self.queryset` and a `pk` AND `slug` argument in the URLconf.
        """
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None and slug is not None:
            queryset = queryset.filter(pk=pk, slug=slug)

        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
            if obj.is_public is False or obj.status != Project.STATUS.published:
                if (
                    self.request.user.is_authenticated
                    and self.request.user.is_superuser
                ):
                    return obj
                else:
                    raise PermissionDenied()
        except queryset.model.DoesNotExist:
            raise Http404()
        return obj

    def get_queryset(self):
        queryset = Project.objects.prefetch_related("suggested_aid").prefetch_related(
            "aid_set"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["aid_set"] = self.object.aid_set.all()
        context["public_project_page"] = True
        context["AidProject"] = AidProject.objects.filter(project=self.object.pk)
        context["suggest_aid_form"] = SuggestAidMatchProjectForm
        if (
            self.request.user.is_authenticated
            and self.request.user.beneficiary_organization
            in self.object.organizations.all()
        ):
            context["organization_own_project"] = True
        if (
            self.request.user.is_authenticated
            and self.request.user.beneficiary_organization
            in self.object.organization_favorite.all()
        ):
            context["organization_favorite_project"] = True
        return context


class FavoriteProjectDetailView(ContributorAndProfileCompleteRequiredMixin, DetailView):
    template_name = "projects/favorite_project_detail.html"
    context_object_name = "project"

    def get_object(self, queryset=None):
        """
        Require `self.queryset` and a `pk` AND `slug` argument in the URLconf.
        """
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None and slug is not None:
            queryset = queryset.filter(pk=pk, slug=slug)

        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
            if (
                obj.is_public is False
                or obj.status != Project.STATUS.published
                or self.request.user.beneficiary_organization
                not in obj.organization_favorite.all()
            ):
                raise PermissionDenied()
        except queryset.model.DoesNotExist:
            raise Http404()
        return obj

    def get_queryset(self):
        queryset = Project.objects.prefetch_related("suggested_aid").prefetch_related(
            "aid_set"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorite_project_page"] = True
        context["aid_set"] = self.object.aid_set.all()
        context["AidProject"] = AidProject.objects.filter(project=self.object.pk)
        context["suggest_aid_form"] = SuggestAidMatchProjectForm
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

    def get_object(self, queryset=None):
        """
        Require a `pk` AND `slug` argument in the URLconf.
        """
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        user = self.request.user
        if pk is not None and slug is not None:
            queryset = queryset.filter(pk=pk, slug=slug)

        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
            if user not in obj.organizations.first().beneficiaries.all():
                raise PermissionDenied()
        except queryset.model.DoesNotExist:
            raise Http404()
        return obj

    def get_queryset(self):
        qs = Project.objects.all()
        self.queryset = qs
        return super().get_queryset()

    def form_valid(self, form):
        project = form.save(commit=False)
        if project.is_public is True:
            project.status = Project.STATUS.reviewable
        else:
            project.status = Project.STATUS.draft
        if self.request.FILES:
            images = self.request.FILES.getlist("image")
            for image in images:
                project.image = image
        project.save()
        form.save_m2m()
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
        org_type = self.request.user.beneficiary_organization.organization_type[0]
        org_details = self.request.user.beneficiary_organization.details_completed()
        if org_type == "commune" or org_type == "epci":
            context["org_is_commune_or_epci"] = True
            if org_details:
                context["org_details_completed"] = True
        return context


class ProjectExportView(ContributorAndProfileCompleteRequiredMixin, DetailView):
    """Export an existing project."""

    context_object_name = "project"

    def get_queryset(self):
        queryset = Project.objects.prefetch_related("aid_set")
        return queryset

    def post(self, request, *args, **kwargs):
        file_format = request.POST["format"]
        project = self.get_object()

        if file_format in EXPORT_FORMAT_KEYS:
            response_data = export_project(project, file_format)
            if "error" not in response_data:
                filename = response_data["filename"]
                return HttpResponse(
                    response_data["content"],
                    content_type=response_data["content_type"],
                    headers={
                        "Content-Disposition": f'attachment; filename="{filename}"'
                    },
                )
        # If something went wrong, redirect to the project page with an error
        messages.error(
            request,
            f"""
            Impossible de générer votre export. Si le problème persiste, merci de
            <a href="{reverse('contact')}"/>nous contacter</a>.
            """,
        )
        return redirect(project)
