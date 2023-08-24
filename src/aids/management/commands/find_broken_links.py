import logging

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site
from aids.utils import check_if_url_returns_an_error


class Command(BaseCommand):
    """Check the reliability of aid associated links"""

    def handle(self, *args, **options):
        from aids.models import Aid

        logger = logging.getLogger("console_log")
        logger.info("Command find_broken_links starting")

        aids = Aid.objects.filter(has_broken_link=False).live()

        nb_links = 0
        aids_list = []
        site = Site.objects.get_current()
        domain = site.domain

        for aid in aids:
            logger.info(f"check for aid_id {aid.id} links")
            if aid.origin_url and check_if_url_returns_an_error(aid.origin_url):
                nb_links += 1
                aids_list.append(aid)
                aid.has_broken_link = True
                aid.save()
                logger.info(f"{aid.name} contains a broken 'origin_url' link")
            if aid.application_url and check_if_url_returns_an_error(
                aid.application_url
            ):
                nb_links += 1
                aids_list.append(aid)
                aid.has_broken_link = True
                aid.save()
                logger.info(f"{aid.name} contains a broken 'application_url' link")

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
        logger.info("email sent")
