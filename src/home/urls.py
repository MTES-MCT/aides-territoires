from django.urls import path
from django.views.generic import TemplateView

from home.views import (
    HomeView,
    ContactView,
    NewsletterConfirmView,
    NewsletterSuccessView,
    ADDNAOptin,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="contact"),
    path(
        "mentions-légales/",
        TemplateView.as_view(template_name="home/legal_mentions.html"),
        name="legal_mentions",
    ),
    path(
        "politique-de-confidentialité/",
        TemplateView.as_view(template_name="home/privacy_policy.html"),
        name="privacy_policy",
    ),
    path(
        "conditions-generales-dutilisation/",
        TemplateView.as_view(template_name="home/cgu.html"),
        name="cgu",
    ),
    path(
        "plan-du-site/",
        TemplateView.as_view(template_name="home/sitemap.html"),
        name="sitemap",
    ),
    path(
        "accessibilité/",
        TemplateView.as_view(template_name="home/accessibility.html"),
        name="accessibility",
    ),
    path(
        "inscription-newsletter-a-confirmer/",
        NewsletterConfirmView.as_view(),
        name="confirm-registration-newsletter",
    ),
    path(
        "inscription-newsletter-succes/",
        NewsletterSuccessView.as_view(),
        name="register_newsletter_success",
    ),
    path("alertes-addna-optin/", ADDNAOptin.as_view(), name="addna_optin"),
]
