from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from braces.views import MessageMixin

from alerts.tasks import send_alert_confirmation_email
from alerts.forms import AlertForm
from alerts.models import Alert


class AlertMixin:

    def get_queryset(self):
        qs = Alert.objects \
            .filter(owner=self.request.user) \
            .order_by('-date_created')
        return qs


class AlertCreate(MessageMixin, CreateView):
    """Create a alert by saving a search view querystring."""

    http_method_names = ['post']
    form_class = AlertForm

    def form_valid(self, form):
        alert = form.save()
        send_alert_confirmation_email.delay(alert.email, alert.token)
        message = _('We just sent you an email to validate your address.')
        self.messages.success(message)
        redirect_url = reverse('search_view')
        return HttpResponseRedirect('{}?{}'.format(
            redirect_url, alert.querystring))

    def form_invalid(self, form):
        msg = _('We could not create your alert because of those '
                'errors: {}').format(form.errors.as_text())
        self.messages.error(msg)
        redirect_url = reverse('search_view')
        return HttpResponseRedirect(redirect_url)


class AlertValidate(DeleteView):
    pass


class AlertDelete(LoginRequiredMixin, MessageMixin, AlertMixin,
                  DeleteView):
    success_url = reverse_lazy('alert_list_view')

    def delete(self, *args, **kwargs):
        res = super().delete(*args, **kwargs)
        self.messages.success(_('Your alert was deleted.'))
        return res
