from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin

from home.forms import ContactForm
from home.tasks import send_contact_form_email
from aids.models import Aid
from backers.models import Backer
from categories.models import Category


class HomeView(TemplateView):
    """Display the home page, as well as some other pages
    (contact form, mailing list registration form, ...)

    Said mailing list is directly posted to the email provider, so we don't
    have to process it ourselves.

    """
    http_method_names = ['get']
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        aids_qs = Aid.objects.live()
        selected_backers = Backer.objects.can_be_displayed_in_carousel()
        # We only display the first 15
        subset_selected_backers = selected_backers.order_by("?")[0:15]
        context = super().get_context_data(**kwargs)
        context['nb_aids'] = aids_qs.values('id').count()
        context['nb_categories'] = Category.objects.all().count()
        context['nb_backers'] =  Backer.objects.has_financed_aids().count()
        context['subset_selected_backers'] = subset_selected_backers

        return context


class ContactView(SuccessMessageMixin, FormView):
    """Display the contact form."""

    form_class = ContactForm
    template_name = 'home/contact.html'
    success_message = 'Votre message a bien été envoyé, merci !'
    success_url = reverse_lazy('contact')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['first_name'] = self.request.user.first_name
            initial['last_name'] = self.request.user.last_name
            initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        """Send the content of the form via email."""
        response = super().form_valid(form)
        form_dict = form.cleaned_data
        send_contact_form_email.delay(form_dict)
        # track_goal(self.request.session, settings.GOAL_CONTACT_ID)
        return response


class NewsletterConfirmView(TemplateView):
    """Display success message after register action."""

    template_name = 'home/newsletter_confirm.html'


class NewsletterSuccessView(TemplateView):
    """Display success message after register action."""

    template_name = 'home/newsletter_success.html'


class ADDNAOptin(TemplateView):
    """Display a welcome message to users from addna."""

    template_name = 'home/addna_optin.html'
