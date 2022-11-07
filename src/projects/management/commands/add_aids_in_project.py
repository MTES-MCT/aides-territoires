import logging
import codecs
import csv
from contextlib import closing

import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Add multiple aids to a project from a distant csv"

    def add_arguments(self, parser):
        parser.add_argument("--url")
        parser.add_argument("--project_id")
        parser.add_argument("--creator_id")

    def handle(self, *args, **options):
        from projects.models import Project
        from aid.models import Aid, Aidproject
        from accounts.models import User

        logger = logging.getLogger("console_log")
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.debug("Command add multiple aids to a project from CSV starting")

        csv_url = options["url"]
        project = Project.objects.get(id=options["project_id"])
        creator = User.objects.get(id=options["creator_id"])

        with closing(requests.get(csv_url, stream=True)) as response:
            csv_content = codecs.iterdecode(response.iter_lines(), "utf-8")
            aids_reader = csv.DictReader(csv_content, delimiter=";")

            for csv_aid in aids_reader:
                logger.info(
                    f"aid = {csv_aid['lien'].strip()}"
                )
                aid_link = csv_aid["lien"].strip()
                aid_slug = str(csv_aid["lien"].strip().partition("https://aides-territoires.beta.gouv.fr/aides/")[1])
                aid_slug = str(aid_slug.partition("/")[0])

                if Aid.objects.filter(slug=aid_slug).exists():

                    aid = Aid.objects.get(slug=aid_slug)
                    Aidproject.objects.create(
                        project=project,
                        aid=aid,
                        creator=creator,
                    )
                    logger.info(
                        f"aidproject created"
                    )
                else:
                    logger.info(
                        f"aid {aid_link} doesn't exists"
                    )
