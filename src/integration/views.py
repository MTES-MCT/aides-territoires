from django.views.generic import TemplateView


class GuyaneGouvView(TemplateView):
    template_name = 'integration/guyane.html'


class SommeView(TemplateView):
    template_name = 'integration/somme.html'
