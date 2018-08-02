from django.views.generic import FormView

from home.forms import MailingListForm


class HomeView(FormView):
    """Display the home page and the mailing list registration form.

    Said mailing list is directly posted to the email provider, so we don't
    have to process it ourselves.

    """
    http_method_names = ['get']
    template_name = 'home/home.html'
    form_class = MailingListForm
