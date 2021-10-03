from django.conf import settings
from django.views.generic import CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from braces.views import AnonymousRequiredMixin

from organizations.forms import OrganizationCreateForm
from accounts.tasks import send_connection_email
from accounts.models import User
from analytics.utils import track_goal


class OrganizationCreateView(AnonymousRequiredMixin, CreateView):

    template_name = 'organizations/create.html'
    form_class = OrganizationCreateForm
    context_object_name = 'organization'

    def form_valid(self, form):
        user_email = self.request.session.get('USER_EMAIL', '')

        organization = form.save(commit=False)
        organization.save()
        form.save_m2m()

        for user in User.objects.filter(email=user_email):
            user_id = user.id
            organization.beneficiaries.add(user_id)

        send_connection_email.delay(user_email)
        track_goal(self.request.session, settings.GOAL_REGISTER_ID)
        msg = "Vous êtes bien enregistré!"
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        success_url = reverse('register_success')
        return success_url
