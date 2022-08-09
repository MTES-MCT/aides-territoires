from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied


from accounts.mixins import ContributorAndProfileCompleteRequiredMixin

from organizations.forms import OrganizationCreateForm, OrganizationUpdateForm
from accounts.models import User
from organizations.models import Organization


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
