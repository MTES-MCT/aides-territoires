# flake8: noqa
import os
from datetime import datetime
from xml.etree import ElementTree

from dataproviders.constants import IMPORT_LICENCES
from dataproviders.utils import content_prettify
from dataproviders.management.commands.base import BaseImportCommand
from geofr.models import Perimeter
from aids.models import Aid

ADDNA = "Aides pour le Développement Durable en Nouvelle-Aquitaine"

ADMIN_ID = 1
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

ELIGIBILITY_TXT = """Consultez la page de l'aide pour obtenir des détails."""
CONTACT_TXT = """A remplir"""

# Convert ADDNA's `perimeter` to our `perimeters`
PERIMETERS_DICT = {
    "International": None,
    "Europe": Perimeter.objects.get(code="EU"),
    "National": Perimeter.objects.get(code="FRA"),
    "Nouvelle - Aquitaine": Perimeter.objects.get(
        code="75", scale=Perimeter.SCALES.region
    ),
    "Creuse (23)": Perimeter.objects.get(code="23"),
    "Corrèze (19)": Perimeter.objects.get(code="19"),
    "Corrèze (19800)": Perimeter.objects.get(code="19"),
    "Haute-Vienne (87)": Perimeter.objects.get(code="87"),
    "Gironde (33)": Perimeter.objects.get(code="33"),
    "Landes (40)": Perimeter.objects.get(code="40"),
    "Pyrénées-Atlantiques (64)": Perimeter.objects.get(code="64"),
    "Charente-Maritime (17)": Perimeter.objects.get(code="17"),
    "Loire-Bretagne": Perimeter.objects.get(code="04", scale=Perimeter.SCALES.basin),
    "Adour Garonne": Perimeter.objects.get(code="05", scale=Perimeter.SCALES.basin),
    "Communauté d’Agglomération de La Rochelle": Perimeter.objects.get(
        code="241700434"
    ),
}


class Command(BaseImportCommand):
    """
    Import data from the Nouvelle-Aquitaine ADDNA data file (xml).
    The file is a one-time export so this script will probably be run only once.
    Fields not extracted:
    - 'tags': too many values
    - 'start_date': always Null
    - 'targeted_audiances': Null or too many values
    """

    def add_arguments(self, parser):
        parser.add_argument("data-file", nargs=1, type=str)

    def fetch_data(self, **options):
        data_file = os.path.abspath(options["data-file"][0])
        xml_tree = ElementTree.parse(data_file)
        xml_root = xml_tree.getroot()
        for xml_elt in xml_root.find("database"):
            # transform xml "database > table > columns" into dict
            table_dict = {}
            for i, column in enumerate(xml_elt.findall("column")):
                column_text = (
                    None if (column.text in ["NULL", None]) else column.text.strip()
                )
                table_dict[column.attrib["name"]] = column_text
            yield table_dict

    def handle(self, *args, **options):
        self.france = Perimeter.objects.get(code="FRA")
        super().handle(*args, **options)

    def line_should_be_processed(self, line):
        return True

    def extract_author_id(self, line):
        return ADMIN_ID

    def extract_import_uniqueid(self, line):
        data_id = line["id"]
        unique_id = "ADDNA_{}".format(data_id)
        return unique_id

    def extract_import_data_url(self, line):
        return None

    def extract_import_share_licence(self, line):
        return IMPORT_LICENCES.unknown

    def extract_name(self, line):
        """name max_length is 180"""
        title = line["name"][:180]
        return title

    def extract_description(self, line):
        description = content_prettify(line["description"])
        return description

    def extract_submission_deadline(self, line):
        submission_deadline_text = line["submission_deadline"]
        if submission_deadline_text:
            submission_deadline = datetime.strptime(
                submission_deadline_text, DATETIME_FORMAT
            ).date()
            return submission_deadline

    def extract_origin_url(self, line):
        origin_url = line["origin_url"]
        if not origin_url:
            return ""  # error if None
        clean_url = origin_url.replace(" ", "%20")
        return clean_url

    def extract_eligibility(self, line):
        # return line['eligibility'] # NULL
        return ELIGIBILITY_TXT

    def extract_contact(self, line):
        return line["contact"] or CONTACT_TXT  # sometimes empty

    def extract_date_published(self, line):
        date_published_text = line["date_created"]
        date_published = datetime.strptime(date_published_text, DATETIME_FORMAT).date()
        return date_published

    def extract_perimeter(self, line):
        """Extract the perimeter value."""
        if line["perimeter"] is None:
            return self.france
        perimeter_text = line["perimeter"].strip()
        if perimeter_text in PERIMETERS_DICT:
            return PERIMETERS_DICT[perimeter_text]

    def extract_financers(self, line):
        return []  # error if None

    def extract_project_examples(self, line):
        """Use the project_examples textfield to store metadata"""
        content = ""
        metadata = {
            "backers": "Porteur",
            "targeted_audiances": "Bénéficiaires",
            "tags": "Tags",
            "perimeter": "Périmètre",
        }
        for elem in metadata:
            if line[elem]:
                content += "<strong>{}</strong>: {}<br /><br />".format(
                    metadata[elem], line[elem]
                )
        return content
