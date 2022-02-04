import requests
import json
from django.conf import settings
from django.contrib import messages
from django.views.generic import CreateView, DetailView, DeleteView, ListView, View
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404

from braces.views import MessageMixin
from accounts.mixins import ContributorAndProfileCompleteRequiredMixin

from alerts.tasks import send_alert_confirmation_email
from alerts.forms import AlertForm, DeleteAlertForm
from alerts.models import Alert


class AlertCreate(MessageMixin, CreateView):
    """Create a alert by saving a search view querystring."""

    http_method_names = ['post']
    form_class = AlertForm

    def form_valid(self, form):
        alert = form.save(commit=False)
        if self.request.user.is_authenticated:
            alert.validated = True
        alert.save()

        if not self.request.user.is_authenticated:
            send_alert_confirmation_email.delay(alert.email, alert.token)
            message = 'Nous venons de vous envoyer un e-mail afin de valider votre alerte.'
        else: 
            message = 'Votre alerte a bien été créée&nbsp;!'
        self.messages.success(message)
        redirect_url = reverse('search_view')
        if alert.source == 'aides-territoires':
            redirect_url += '?{}'.format(alert.querystring)
        return HttpResponseRedirect(redirect_url)

    def form_invalid(self, form):
        querystring = form.cleaned_data.get('querystring', '')
        source = form.cleaned_data.get('source', 'aides-territoires')
        msg = _('Nous n\'avons pas pu enregistrer votre alerte à cause de ces '
                'erreurs : {}').format(form.errors.as_text())
        self.messages.error(msg)
        redirect_url = reverse('search_view')
        if source == 'aides-territoires':
            redirect_url += '?{}'.format(querystring)
        return HttpResponseRedirect(redirect_url)


class AlertValidate(MessageMixin, DetailView):
    """Confirms that the alert email is valid."""

    model = Alert
    slug_field = 'token'
    slug_url_kwarg = 'token'
    context_object_name = 'alert'
    template_name = 'alerts/validate.html'

    def post(self, *args, **kwargs):
        """Validates the alert."""

        alert = self.get_object()
        if not alert.validated:
            alert.validate()
            alert.save()

        msg = _('You confirmed the alert creation.')
        self.messages.success(msg)

        redirect_url = '{}?{}'.format(reverse('search_view'), alert.querystring)
        return HttpResponseRedirect(redirect_url)


class AlertDelete(MessageMixin, DeleteView):
    """Alert deletion view.

    Since we don't require a login to create alert, no authentication is
    required to delete them either.

    If you know the secret alert token, we suppose you are the owner, thus
    you can delete it.
    """
    model = Alert
    slug_field = 'token'
    slug_url_kwarg = 'token'
    context_object_name = 'alert'
    template_name = 'alerts/confirm_delete.html'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset=queryset)
        except ValidationError:
            raise Http404()

    def get_success_url(self):
        if self.request.user.is_authenticated:
            url = reverse('alert_list_view')
        else:
            url = '{}?{}'.format(reverse('search_view'), self.object.querystring)
        return url

    def delete(self, *args, **kwargs):
        res = super().delete(*args, **kwargs)
        msg = format_html(
            "Votre alerte vient d'être supprimée.<br />"
            "Pour nous aider à mieux comprendre votre choix, pourriez-vous nous expliquer la raison de votre désabonnement "  # noqa
            f'<a href="{settings.ALERT_DELETE_FEEDBACK_FORM_URL}" target="_blank" rel="noopener">ici</a> ?')  # noqa
        self.messages.success(msg)
        return res


class AlertListView(ContributorAndProfileCompleteRequiredMixin, ListView):
    """User Alerts Dashboard"""

    template_name = 'accounts/user_alert_dashboard.html'
    context_object_name = 'alerts'

    def get_queryset(self):
        queryset = Alert.objects \
            .filter(email=self.request.user.email)
        return queryset

    def isUserSubscriber(self):
        '''
        Here we want to check if user is already a newsletter's subscriber.
        '''

        url = "https://api.sendinblue.com/v3/contacts/" + self.request.user.email

        headers = {
            "Accept": "application/json",
            "api-key": settings.SIB_API_KEY,
        }

        response = requests.request("GET", url, headers=headers)

        if response:
            r_text = json.loads(response.text)
            r_listIds = r_text['listIds']
            if 'DOUBLE_OPT-IN' in r_text['attributes']:
                r_double_opt_in = r_text['attributes']['DOUBLE_OPT-IN']
            else:
                r_double_opt_in = "1"
            # If user exists, and if double-opt-in is true,
            # and if user is associated to the newsletter list id
            # Then, user is already a newsletter's subscriber
            SIB_NEWSLETTER_LIST_IDS = settings.SIB_NEWSLETTER_LIST_IDS.split(', ')
            SIB_NEWSLETTER_LIST_IDS = [int(i) for i in SIB_NEWSLETTER_LIST_IDS]
            IsInNewsletterList = any((True for x in SIB_NEWSLETTER_LIST_IDS if x in r_listIds))
            if r_double_opt_in == "1" and IsInNewsletterList:
                return True
            else:
                return False
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isUserSubscriber'] = self.isUserSubscriber
        return context


class AlertDeleteFromAccountView(ContributorAndProfileCompleteRequiredMixin, View):
    """Allow user to delete an alert"""

    form_class = DeleteAlertForm
    template_name = 'accounts/user_alert_dashboard.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            alert_token = form.cleaned_data['token']
            try:
                alert = Alert.objects.get(pk=alert_token, email=self.request.user.email)
                alert.delete()
                msg = "Votre alerte a bien été supprimée."
                messages.success(self.request, msg)
            except:
                msg = "Une errreur s'est produite lors de la suppression de votre alerte"
                messages.error(self.request, msg)
            success_url = reverse('alert_list_view')
            return HttpResponseRedirect(success_url)
        
        return render(request, self.template_name, {'form': form})
