from django.views.generic import TemplateView
from django.db.models import Q

from aids.models import Aid
from backers.models import Backer
from categories.models import Category


class HomeView(TemplateView):
    """Display the home page and the mailing list registration form.

    Said mailing list is directly posted to the email provider, so we don't
    have to process it ourselves.

    """
    http_method_names = ['get']
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):

        aids_qs = Aid.objects.open().published()
        financers = aids_qs.values_list('financers', flat=True)
        instructors = aids_qs.values_list('instructors', flat=True)
        nb_backers = Backer.objects \
            .filter(Q(id__in=financers) | Q(id__in=instructors)) \
            .values('id') \
            .count()
        selected_backers = Backer.objects \
            .filter(Q(logo__isnull=False) & Q(is_spotlighted=True))
        random_backers = selected_backers.order_by("?")[0:12]
        
        context = super().get_context_data(**kwargs)
        context['nb_aids'] = aids_qs.values('id').count()
        context['nb_categories'] = Category.objects.all().count()
        context['nb_backers'] = nb_backers
        context['random_backers'] = random_backers

        return context


class NewsletterConfirmView(TemplateView):
    """Display success message after register action."""

    template_name = 'home/newsletter_confirm.html'


class NewsletterSuccessView(TemplateView):
    """Display success message after register action."""

    template_name = 'home/newsletter_success.html'


class ADDNAOptin(TemplateView):
    """Display a welcome message to users from addna."""

    template_name = 'home/addna_optin.html'
