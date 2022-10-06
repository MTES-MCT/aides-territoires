# flake8: noqa

import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand

from aids.models import Aid
from backers.models import Backer


TIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"


# Perimeter values conversion matrix
PERIMETERS = {
    "commune": "commune",
    "departement": "department",
    "region": "region",
    "metropole": "mainland",
    "outre_mer": "overseas",
    "france": "france",
    "europe": "europe",
}

STEPS = {
    "pre_operationnel": "preop",
    "operationnel": "op",
    "fonctionnement": "postop",
}

AUDIENCES = {
    "commune": "commune",
    "departement": "department",
    "region": "region",
    "EPCI": "epci",
    "entreprises": "company",
    "societe_civile": "civil_society",
    "associations": "association",
    "autre": "other",
}

TYPES = {
    "subvention": "grant",
    "convention": "convention",
    "formation": "training",
    "bonification_interet": "interest_subsidy",
    "pret": "loan",
    "avance_recuperable": "recoverable_advance",
    "garantie": "guarantee",
    "pret_taux_reduit": "low_interest_rate_loan",
    "investissement_en_capital": "capital_investment",
    "avantage_fiscal": "tax_benefit",
    "fonds_de_retour": "return_fund",
    "ingenierie": "engineering",
    "conseil": "guidance",
    "accompagnement": "accompaniment",
    "valorisation": "valorisation",
    "communication": "communication",
    "autre": "other",
}

DESTINATIONS = {
    "investissement": "investment",
    "fonctionnement": "supply",
    "etude": "supply",
    "fourniture": "supply",
    "service": "supply",
    "travaux": "supply",
    "autre": "supply",
}

THEMATICS = {
    "amenagement_durable": "sustainable_management",
    "developpement_local": "local_development",
    "infrastructures_reseaux_et_deplacements": "infrastructure_networks",
    "solidarite_et_cohesion_sociale": "solidarity_social_cohesion",
}

STATUSES = {
    "ouvert": "open",
    "projete": "planned",
    "ferme": "closed",
}


class Command(BaseCommand):
    """Imports old data into the new base.

    In the project's first version, a no-sql mongo database was used. This
    script is made to import this data into today's django model.

    Note: since this script is designed to be run once and then forgotten,
    tests and quality are left to the minimum.
    """

    def add_arguments(self, parser):
        parser.add_argument("json_file", nargs=1, type=str)

    def handle(self, *args, **options):

        json_file = os.path.abspath(options["json_file"][0])
        json_data = json.load(open(json_file))
        for datum in json_data:
            self.import_aid(datum)

    def import_field(self, data, old_field_name, aid, new_field_name):
        if old_field_name in data and data[old_field_name]:
            field_value = data[old_field_name]
            setattr(aid, new_field_name, field_value)
        return

    def import_aid(self, data):
        backer, _ = Backer.objects.get_or_create(name=data["structurePorteuse"])

        aid = Aid()
        aid.author_id = 1
        aid.backer = backer
        aid.status = "published"

        self.import_field(data, "nom", aid, "name")
        self.import_field(data, "description", aid, "description")
        self.import_field(data, "criteresEligibilite", aid, "eligibility")
        self.import_field(data, "lien", aid, "url")
        self.import_field(data, "nom", aid, "name")
        self.import_field(data, "nom", aid, "name")
        self.import_field(data, "populationMin", aid, "minimal_population")
        self.import_field(data, "populationMax", aid, "maximal_population")
        self.import_field(data, "beneficiairesAutre", aid, "targeted_audiences_detail")
        self.import_field(data, "", aid, "targeted_audiences_detail")
        self.import_field(data, "beneficiairesAutre", aid, "targeted_audiences_detail")
        self.import_field(data, "formeDeDiffusionAutre", aid, "aid_types_detail")
        self.import_field(data, "destinationAutre", aid, "destinations_detail")
        self.import_field(data, "beneficiairesAutre", aid, "targeted_audiences_detail")
        self.import_field(data, "tauxSubvention", aid, "subvention_rate")
        self.import_field(data, "contact", aid, "contact_detail")

        aid.mobilization_steps = self.get_mobilization_steps(data)
        aid.targeted_audiences = self.get_audiences(data)
        aid.aid_types = self.get_types(data)
        aid.destinations = self.get_destinations(data)
        aid.thematics = self.get_thematics(data)
        aid.publication_status = self.get_status(data)

        aid.application_perimeter = self.get_application_perimeter(data)
        if aid.application_perimeter == "region":
            aid.application_region = data["perimetreApplicationCode"]
        elif aid.application_perimeter == "department":
            aid.application_department = data["perimetreApplicationCode"]

        aid.is_funding = data["type"] == "financement"

        if "demandeTiersPossible" in data:
            aid.open_to_third_party = data["demandeTiersPossible"] is not None

        if "dateDebut" in data and data["dateDebut"]:
            aid.start_date = datetime.strptime(data["dateDebut"]["$date"], TIME_FMT)

        if "datePredepot" in data and data["datePredepot"]:
            aid.predeposit_date = datetime.strptime(
                data["datePredepot"]["$date"], TIME_FMT
            )

        if "dateEcheance" in data and data["dateEcheance"]:
            aid.submission_deadline = datetime.strptime(
                data["dateEcheance"]["$date"], TIME_FMT
            )

        aid.save()

    def get_application_perimeter(self, data):
        original_perimeter = data["perimetreApplicationType"]
        return PERIMETERS[original_perimeter]

    def get_mobilization_steps(self, data):
        original_steps = data["etape"]
        steps = [STEPS[original_step] for original_step in original_steps]
        return steps

    def get_audiences(self, data):
        original_audiences = data["beneficiaires"]
        audiences = [
            AUDIENCES[original_audience] for original_audience in original_audiences
        ]
        return audiences

    def get_types(self, data):
        original_types = data["formeDeDiffusion"]
        types = [TYPES[original_type] for original_type in original_types]
        return types

    def get_destinations(self, data):
        original_destinations = data["destination"]
        destinations = [
            DESTINATIONS[original_destination]
            for original_destination in original_destinations
        ]
        return destinations

    def get_thematics(self, data):
        original_thematics = data["thematiques"]
        thematics = [
            THEMATICS[original_thematic] for original_thematic in original_thematics
        ]
        return thematics

    def get_status(self, data):
        if "status" in data:
            original_status = data["status"]
            new_status = STATUSES[original_status]
        else:
            new_status = "unknown"

        return new_status
