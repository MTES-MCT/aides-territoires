import os
import json
import requests

from django.utils import timezone

from dataproviders.models import DataSource
from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify, get_category_list_from_name
from dataproviders.management.commands.base import BaseImportCommand
from aids.models import Aid

ADMIN_ID = 1

DATA_SOURCE = DataSource.objects.prefetch_related("perimeter", "backer").get(pk=9)

FEED_ROWS = 1000


class Command(BaseImportCommand):
    """
    Import data from the Conseil Départemental de la Drôme Data plateform.
    """

    def add_arguments(self, parser):
        parser.add_argument("data-file", nargs="?", type=str)

    def handle(self, *args, **options):
        DATA_SOURCE.date_last_access = timezone.now()
        DATA_SOURCE.save()
        super().handle(*args, **options)

    def fetch_data(self, **options):
        if options["data-file"]:
            data_file = os.path.abspath(options["data-file"])
            data = json.load(open(data_file))
            for line in data["results"]:
                yield line
        else:
            req = requests.get(DATA_SOURCE.import_api_url)
            req.encoding = (
                "utf-8-sig"  # We need this to take care of the bom (byte order mark)
            )
            data = json.loads(req.text)
            self.stdout.write("Total number of aids: {}".format(data["count"]))
            if data["count"] > FEED_ROWS:
                self.stdout.write(
                    self.style.ERROR(
                        "Only fetching {} aids, but there are {} aids".format(
                            FEED_ROWS, data["count"]
                        )
                    )
                )
            self.stdout.write(
                "Number of aids processing: {}".format(len(data["results"]))
            )
            for line in data["results"]:
                yield line

    def line_should_be_processed(self, line):
        return True

    def extract_import_data_source(self, line):
        return DATA_SOURCE

    def extract_import_uniqueid(self, line):
        unique_id = "CDDr_{}".format(line["id"])
        return unique_id

    def extract_import_data_url(self, line):
        return DATA_SOURCE.import_data_url

    def extract_import_share_licence(self, line):
        return DATA_SOURCE.import_licence or IMPORT_LICENCES.unknown

    def extract_author_id(self, line):
        return DATA_SOURCE.aid_author_id or ADMIN_ID

    def extract_import_raw_object_calendar(self, line):
        import_raw_object_calendar = {}
        if line.get("start_date", None) is not None:
            import_raw_object_calendar["start_date"] = line["start_date"]
        if line.get("predeposit_date", None) is not None:
            import_raw_object_calendar["predeposit_date"] = line["predeposit_date"]
        if line.get("submission_deadline", None) is not None:
            import_raw_object_calendar["submission_deadline"] = line[
                "submission_deadline"
            ]
        if line.get("recurrence", None) is not None:
            import_raw_object_calendar["recurrence"] = line["recurrence"]
        return import_raw_object_calendar

    def extract_import_raw_object(self, line):
        import_raw_object = dict(line)
        if line.get("start_date", None) is not None:
            import_raw_object.pop("start_date")
        if line.get("predeposit_date", None) is not None:
            import_raw_object.pop("predeposit_date")
        if line.get("submission_deadline", None) is not None:
            import_raw_object.pop("submission_deadline")
        if line.get("recurrence", None) is not None:
            import_raw_object.pop("recurrence")
        return import_raw_object

    def extract_recurrence(self, line):
        if line.get("recurrence", None) is not None:
            if line.get("recurrence") == "Permanente":
                recurrence = Aid.RECURRENCES.ongoing
            if line.get("recurrence") == "Ponctuelle":
                recurrence = Aid.RECURRENCES.oneoff
            if line.get("recurrence") == "Récurrente":
                recurrence = Aid.RECURRENCES.recurring
        return recurrence

    def extract_name(self, line):
        name = line["name"][:180]
        return name

    def extract_name_initial(self, line):
        name_initial = line["name"][:180]
        return name_initial

    def extract_description(self, line):
        description = line["description"]
        str_to_find = "Service Instructeur et Référent"
        if str_to_find in description:
            description = str(line.get("description", "").partition(str_to_find)[0])
            description = content_prettify(description)
        return description

    def extract_eligibility(self, line):
        str_to_find = "Opérations éligibles"
        if str_to_find in line.get("description", ""):
            eligibility_1 = str(line.get("description", "").partition(str_to_find)[1])
            eligibility_2 = str(line.get("description", "").partition(str_to_find)[2])
            eligibility_3 = str(eligibility_2.partition("Type d’aide")[0])
            eligibility = "<h3><strong>" + eligibility_1 + eligibility_3
            eligibility = content_prettify(eligibility)
            return eligibility
        else:
            return ""

    def extract_financers(self, line):
        return [DATA_SOURCE.backer]

    def extract_perimeter(self, line):
        return DATA_SOURCE.perimeter

    def extract_origin_url(self, line):
        origin_url = line["origin_url"]
        return origin_url

    def extract_application_url(self, line):
        application_url = line["application_url"]
        return application_url

    def extract_aid_types(self, line):
        types = line.get("aid_types", None)
        aid_types = []
        for type_item in types:
            types = next(choice[0] for choice in Aid.TYPES if choice[1] == type_item)
            aid_types.append(types)
        return aid_types

    def extract_is_call_for_project(self, line):
        is_call_for_project = True
        return is_call_for_project

    def extract_start_date(self, line):
        if line.get("start_date", None) is not None:
            start_date = line.get("start_date", None)
            return start_date

    def extract_submission_deadline(self, line):
        if line.get("submission_deadline", None) is not None:
            submission_deadline = line.get("submission_deadline", None)
            return submission_deadline

    def extract_targeted_audiences(self, line):
        """
        Exemple of string to process:
        [
            "Communes",
            "Intercommunalités / Pays",
            "Associations",
            "Particuliers"
        ]
        """
        targeted_audiences = line.get("targeted_audiences", None)
        name = line["name"][:180]
        aid_targeted_audiences = []
        if targeted_audiences is not None:
            if targeted_audiences != []:
                for targeted_audience in targeted_audiences:
                    try:
                        targeted_audience = next(
                            choice[0]
                            for choice in Aid.AUDIENCES
                            if choice[1] == targeted_audience
                        )
                        aid_targeted_audiences.append(targeted_audience)
                    except Exception:
                        print(f"{targeted_audience}")
            else:
                print(f"{name} aucun bénéficiaire")
            return aid_targeted_audiences

    def extract_categories(self, line):
        """
        Exemple of string to process: [
                "B\u00e2timents et construction",
                "Foncier",
                "Logement et habitat",
                "Equipement public",
                "Voirie"
            ]
        """
        categories = line.get("categories", None)
        name = line["name"][:180]
        aid_categories = []
        if categories != []:
            for category in categories:
                try:
                    get_category_list_from_name(category)
                    aid_categories.extend(get_category_list_from_name(category))
                except Exception:
                    print(f"{category}")
        else:
            print(f"{name} aucune thématique")
        return aid_categories

    def extract_contact(self, line):
        str_to_find = "Service Instructeur et Référent"
        if line.get("contact", "") != "":
            contact = line.get("contact")
            return content_prettify(contact)
        elif str_to_find in line.get("description", ""):
            contact_1 = str(line.get("description", "").partition(str_to_find)[1])
            contact_2 = str(line.get("description", "").partition(str_to_find)[2])
            contact = "<h3><strong>" + contact_1 + contact_2
            return content_prettify(contact)
        else:
            return ""

    def extract_mobilization_steps(self, line):
        return [Aid.STEPS.op, Aid.STEPS.preop]
