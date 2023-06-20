import csv
from io import StringIO
import logging
import requests

from django.db import transaction
from django.utils import timezone

from geofr.models import Perimeter
from geofr.utils import attach_perimeters

logger = logging.getLogger("console_log")

"""
Our data source comes from the Inventaire national du patrimoine naturel.
https://inpn.mnhn.fr/telechargement/cartes-et-information-geographique/ep/pnr

The actual list of communes belonging to a PNR is in a Google spreadsheet
"""

SHEET_ID = "174-d1Jx3T7jJNiNWC4RApHd5ZiRHL4uUNKIKCCrxd4U"
SHEET_NAME = "liste_communes_pnrf"
DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"  # noqa

# 2023 update: replacing the manually set codes by those sourced from the INPN.
AT_IDS_MAPPING = {
    "FR8000005": "ARMORIQUE PNR",
    "FR8000009": "BRIERE PNR",
    "FR8000011": "CAMARGUE PNR",
    "FR8000004": "PNRC",
    "FR8000012": "CORSE PNR",
    "FR8000040": "GUYANE PNR",
    "FR8000054": "PNRAU",
    "FR8000036": "AVESNOIS PNR",
    "FR8000008": "BRENNE PNR",
    "FR8000013": "FORET ORIENT PNR",
    "FR8000017": "HAUTE VALL PNR",
    "FR8000024": "MONTAGNE PNR",
    "FR8000042": "NARBONNAISE PNR",
    "FR8000020": "LORRAINE PNR",
    "FR8000023": "MARTINIQUE PNR",
    "FR8000045": "MilleVachesPNR",
    "FR8000046": "ALPILLES PNR",
    "FR8000048": "ARDENNES PNR",
    "FR8000006": "BALLONS VOSGES",
    "FR8000052": "BARONNIES PNR",
    "FR8000010": "BOUCLES PNR",
    "FR8000007": "CAPS PNR",
    "FR8000039": "CAUSSES PNR",
    "FR8000014": "GRANDS CAUS PNR",
    "FR8000018": "landesPNR",
    "FR8000041": "MONTS ARDECH PNR",
    "FR8000049": "PNR_Préalpes_Azu",
    "FR8000047": "PYRÉNÉES ARIÉGEO",
    "FR8000044": "PYRENEES CATALAN",
    "FR8000028": "VOLCANS AUVERGNE",
    "FR8000029": "VOSGES PNR",
    "FR8000058": "Doubs",
    "FR8000038": "GATINAIS FR PNR",
    "FR8000051": "GOLFE MORBI PNR",
    "FR8000015": "HAUT-JURA PNR",
    "FR8000016": "HAUT-LANGUE PNR",
    "FR8000003": "LUBERON PNR",
    "FR8000050": "MaraisPNR",
    "FR8000031": "MASSIF BAUGE PNR",
    "FR8000025": "MORVAN PNR",
    "FR8000027": "PILAT PNR",
    "FR8000002": "QUEYRAS PNR",
    "FR8000001": "VERCORS PNR",
    "FR8000033": "VERDON PNR",
    "FR8000030": "VEXIN PNR",
    "FR8000019": "LIVRADOIS-FO PNR",
    "FR8000032": "LOIRE-ANJOU-PNR",
    "FR8000043": "PNROPF",
    "FR8000035": "PERIGORD_PNR",
    "FR8000037": "SCARPE - ESCAUT",
}


def update_pnr_codes() -> None:
    logger.info("Updating PNR codes")
    updated = 0
    for mnhn_id, old_code in AT_IDS_MAPPING.items():
        new_code = f"PNR-{mnhn_id}"
        pnr = Perimeter.objects.filter(
            scale=Perimeter.SCALES.adhoc, code=old_code
        ).first()

        if pnr:
            pnr.code = new_code
            pnr.save()
            updated += 1

    logger.info(f"{updated} PNR codes updated.")


@transaction.atomic
def populate_pnr() -> None:
    """
    Import the list of Parcs naturels régionaux (PNR).
    """
    start_time = timezone.now()

    # 2023 update
    update_pnr_codes()

    pnr_all = {}
    nb_created = 0
    nb_updated = 0
    nb_obsolete = 0

    logger.debug(f"Getting file {DATA_URL} from distant URL")

    response = requests.get(DATA_URL)
    csv_raw = StringIO(response.text)
    reader = csv.DictReader(csv_raw)

    logger.debug("Parsing file…")
    for row in reader:
        pnr_id = row["id_mnhn"]
        if pnr_id not in pnr_all:
            pnr_all[pnr_id] = {"name": row["PNR"], "communes": []}

        pnr_all[pnr_id]["communes"].append(row["insee_com"])

    logger.debug("Importing data for PNRs…")

    for pnr_id in pnr_all.keys():
        # Customizing PNR code
        pnr_code = f"PNR-{pnr_id}"
        pnr_name = f"{pnr_all[pnr_id]['name']} (Parc naturel régional)"
        logger.debug(f"Importing data for {pnr_code} ({pnr_name})")

        # Create or update the SCoT perimeter
        scot, created = Perimeter.objects.update_or_create(
            scale=Perimeter.SCALES.adhoc,
            code=pnr_code,
            defaults={"name": pnr_name, "is_obsolete": False, "date_obsolete": None},
        )
        if created:
            nb_created += 1
        else:
            nb_updated += 1

        codes = pnr_all[pnr_id]["communes"]
        attach_perimeters(scot, codes)

    # Mark obsolete PNRs
    nb_obsolete = Perimeter.objects.filter(
        scale=Perimeter.SCALES.adhoc,
        code__startswith="PNR-",
        date_updated__lt=start_time,
    ).update(is_obsolete=True, date_obsolete=start_time)

    end_time = timezone.now()
    logger.info(f"Import made in {end_time - start_time}.")
    logger.info(f"* {nb_created} entries created")
    logger.info(f"* {nb_updated} entries updated")
    logger.info(f"* {nb_obsolete} entries marked as obsolete")
