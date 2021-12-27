from django.conf import settings
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from accounts.mixins import ContributorAndProfileCompleteRequiredMixin

from organizations.forms import OrganizationCreateForm, OrganizationUpdateForm
from accounts.tasks import send_connection_email
from accounts.models import User
from analytics.utils import track_goal
from organizations.models import Organization


class OrganizationCreateView(CreateView):

    template_name = 'organizations/create.html'
    form_class = OrganizationCreateForm
    context_object_name = 'organization'

    def form_valid(self, form):

        if self.request.session.get('USER_EMAIL'):
            user_email = self.request.session.get('USER_EMAIL')
            user_organization_type = self.request.session.get('USER_ORGANIZATION_TYPE')
        elif self.request.user.email:
            user_email = self.request.user.email
            user_organization_type = self.request.POST.get('organization_type')
        else:
            return

        organization = form.save(commit=False)
        organization.organization_type = [user_organization_type]
        organization.zip_code = organization.perimeter.zipcodes[0]
        organization.city_name = organization.perimeter.name
        organization.save()
        form.save_m2m()

        user_id = User.objects.filter(email=user_email).first().pk
        organization.beneficiaries.add(user_id)
        User.objects.filter(pk=user_id).update(beneficiary_organization=organization.pk)

        if self.request.session.get('USER_EMAIL'):
            send_connection_email.delay(user_email)
            track_goal(self.request.session, settings.GOAL_REGISTER_ID)
            msg = "Vous êtes bien enregistré&nbsp;!"
            messages.success(self.request, msg)
            success_url = reverse('register_success')
            self.request.session.pop('USER_EMAIL')
            self.request.session.pop('USER_ORGANIZATION_TYPE')

        elif self.request.user.email:
            msg = "Votre profil a bien été mis à jour&nbsp;!"
            messages.success(self.request, msg)
            success_url = reverse('user_dashboard')

        return HttpResponseRedirect(success_url)


class OrganizationUpdateView(ContributorAndProfileCompleteRequiredMixin, UpdateView):

    template_name = 'organizations/update.html'
    form_class = OrganizationUpdateForm
    context_object_name = 'organization'

    def form_valid(self, form):

        organization = form.save(commit=False)
        organization.save()

        msg = "Les informations de votre structure ont bien été mises à jour."
        messages.success(self.request, msg)
        success_url = reverse('organization_update_view', args=[self.object.pk])
        return HttpResponseRedirect(success_url)

    def get_queryset(self):
        qs = Organization.objects.all()
        self.queryset = qs
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.object
        return context
