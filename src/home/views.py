from django.views.generic import TemplateView

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
        context = super().get_context_data(**kwargs)

        context['nb_aids'] = Aid.objects.open().published().count()
        context['nb_backers'] = Backer.objects.all().count()
        context['nb_categories'] = Category.objects.all().count()

        return context
