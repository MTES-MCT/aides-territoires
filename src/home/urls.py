from django.urls import path
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from home.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path(
        _('legal-mentions/'),
        TemplateView.as_view(template_name='home/legal_mentions.html'),
        name='legal_mentions'),
    path(
        _('mailing-list-registration/'),
        TemplateView.as_view(template_name='home/ml_registration.html'),
        name='mailing_list_registration'),
]
