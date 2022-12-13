import requests

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site


class Command(BaseCommand):
    """Check the reliability of aid associated links"""

    def check_if_url_return_a_404(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 404:
                return True
        except Exception:
            return True

    def handle(self, *args, **options):
        from aids.models import Aid

        aids = Aid.objects.filter(has_broken_link=False).live()

        nb_links = 0
        aids_list = []
        site = Site.objects.get_current()
        domain = site.domain

        for aid in aids:
            if aid.origin_url:
                if self.check_if_url_return_a_404(aid.origin_url):
                    nb_links += 1
                    aids_list.append(aid)
                    aid.has_broken_link = True
                    aid.save()
            if aid.application_url:
                if self.check_if_url_return_a_404(aid.application_url):
                    nb_links += 1
                    aids_list.append(aid.get_absolute_url())
                    aid.has_broken_link = True
                    aid.save()

        email_body = render_to_string(
            "emails/find_broken_links.txt",
            {
                "nb_links": nb_links,
                "aids_list": aids_list,
                "domain": domain,
            },
        )
        email_subject = f"{nb_links} liens sont cassés dans des fiches aide"
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [settings.SERVER_EMAIL]

        send_mail(email_subject, email_body, email_from, email_to, fail_silently=False)
