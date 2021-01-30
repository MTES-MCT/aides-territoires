from django.urls import path
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from home.views import (HomeView, NewsletterConfirmView,
                        NewsletterSuccessView, ADDNAOptin)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path(
        _('legal-mentions/'),
        TemplateView.as_view(template_name='home/legal_mentions.html'),
        name='legal_mentions'),

    path(_('confirm-registration-newsletter/'),
         NewsletterConfirmView.as_view(),
         name='confirm-registration-newsletter'),
    path(_('register-newsletter-success/'), NewsletterSuccessView.as_view(),
         name='register_newsletter_success'),

    path('alertes-addna-optin/', ADDNAOptin.as_view(), name='addna_optin'),
]
