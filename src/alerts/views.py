from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from braces.views import MessageMixin

from accounts.forms import RegisterForm
from accounts.models import User
from alerts.tasks import send_alert_confirmation_email
from alerts.forms import AlertForm
from alerts.models import Alert


class AlertMixin:

    def get_queryset(self):
        qs = Alert.objects \
            .filter(owner=self.request.user) \
            .order_by('-date_created')
        return qs


class AlertCreate(MessageMixin, AlertMixin, CreateView):
    """Create a alert by saving a search view querystring.

    This view has to handle four cases:

     1. the user creating the alert is already connected.
     2. the user is just an anonymous visitor.
     3. the user is an anonymous visitor but they already created a
        alert with the same email address.
     4. the user isn't logged in but their email correspond to a known and
        valid account.

    """

    http_method_names = ['post']
    form_class = AlertForm

    @transaction.atomic
    def form_valid(self, form):

        if self.request.user.is_authenticated:
            user_email = self.request.user.email
        else:
            user_email = form.cleaned_data['email']

        try:
            existing_account = User.objects.get(email=user_email)
        except User.DoesNotExist:
            existing_account = None

        if existing_account:
            owner = existing_account
            send_alert = form.cleaned_data.get('send_email_alert', True)
            alert = self.create_alert(form, owner, send_alert)
            alerts_url = reverse('alert_list_view')
            message = _('Your new alert was successfully created. '
                        '<a href="%(url)s">You will find in in your alert '
                        'list.</a>') % {'url': alerts_url}

        else:
            owner = self.create_account(form)
            send_alert = True
            alert = self.create_alert(form, owner, send_alert)
            send_alert_confirmation_email.delay(owner.email, alert.id)
            message = _('We just sent you an email to validate your address.')

        self.messages.success(message)
        redirect_url = reverse('search_view')
        return HttpResponseRedirect('{}?{}'.format(
            redirect_url, alert.querystring))

    def create_alert(self, form, owner, send_alert):
        """Create a new alert."""

        alert = Alert.objects.create(
            owner=owner,
            title=form.cleaned_data['title'],
            send_email_alert=send_alert,
            alert_frequency=form.cleaned_data['alert_frequency'],
            querystring=form.cleaned_data['querystring'])

        return alert

    def create_account(self, form):
        """Create a tmp account to attach the alert to."""

        register_form = RegisterForm({
            'email': form.cleaned_data['email'],
            'full_name': form.cleaned_data['email'],
            'ml_consent': False})
        user = register_form.save()
        return user

    def form_invalid(self, form):
        if form.has_error('email', 'unique'):
            msg = _('An account with this address already exists. If this is '
                    'your account, you might want to login first.')
        else:
            msg = _('We could not create your alert because of those '
                    'errors: {}').format(form.errors.as_text())

        self.messages.error(msg)
        redirect_url = reverse('search_view')
        return HttpResponseRedirect(redirect_url)


class AlertDelete(LoginRequiredMixin, MessageMixin, AlertMixin,
                  DeleteView):
    success_url = reverse_lazy('alert_list_view')

    def delete(self, *args, **kwargs):
        res = super().delete(*args, **kwargs)
        self.messages.success(_('Your alert was deleted.'))
        return res
