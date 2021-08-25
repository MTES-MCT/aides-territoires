import os
import json
import copy

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models.fields import (
    AutoField, PositiveIntegerField,
    CharField, TextField, EmailField, URLField, SlugField,
    BooleanField, DateField, DateTimeField)
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.contrib.postgres.search import SearchVectorField

from django_xworkflows.models import StateField

from aids.models import Aid
from core.fields import ChoiceArrayField, PercentRangeField
# from aids.resources import *


SCHEMA_PATH = 'aids/schema/schema.json'
SCHEMA_PATH_FRENCH = 'aids/schema/schema_fr.json'

SCHEMA_BASE = {
    "$schema": "https://frictionlessdata.io/schemas/table-schema.json",
    "name": "",
    "title": "",
    "description": "Spécification des aides de la plateforme Aides-territoires",
    "keywords": [
        "aide",
        "appel à projet",
        "subvention"
    ],
    "countryCode": "FR",
    "homepage": "",
    "path": "",
    "image": "",
    "licenses": [
        {
        "title": "Licence Ouverte",
        "name": "etalab-2.0",
        "path": "https://www.etalab.gouv.fr/licence-ouverte-open-licence"
        }
    ],
    "resources": [
        {
        "title": "Ressource valide",
        "name": "exemple-valide",
        "path": ""
        }
    ],
    "sources": [],
    "created": "2021-08-25",
    "lastModified": "2021-08-25",
    "version": "0.1.0",
    "contact":settings.CONTACT_EMAIL,
    "uri":"",
    "example":"",
    "contributors": [],
    "fields": []
}

TYPE_MAPPING = {
    CharField: 'string',
    TextField: 'string',
    EmailField: 'string',
    URLField: 'string',
    SlugField: 'string',
    StateField: 'string',
    PercentRangeField: 'string',
    ChoiceArrayField: 'string',  # why not 'array'? because we coerce it to a 'string'
    BooleanField: 'boolean',
    AutoField: 'integer',
    PositiveIntegerField: 'integer',
    DateField: 'date',
    DateTimeField: 'datetime',
    JSONField: 'object',
    # SearchVectorField: 'string',
    ForeignKey: 'string',  # mapped as a CharField
    ManyToManyField: 'string'  # mapped as a ChoiceArrayField
}

STRING_FORMAT_MAPPING = {
    EmailField: 'email',
    URLField: 'uri'
}

BOOLEAN_TRUE_VALUES = ['Oui', 'Vrai', 'Yes', 'True']
BOOLEAN_FALSE_VALUES = ['Non', 'Faux', 'No', 'False']

EXCLUDED_FIELDS = [
    'search_vector_unaccented', 'eligibility_test', 'instructor_suggestion', 'perimeter_suggestion',
    'is_imported', 'import_data_source', 'import_uniqueid', 'import_data_url', 'import_share_licence', 'import_last_access', 'import_raw_object',  # noqa
    'is_amendment', 'amended_aid', 'amendment_author_name', 'amendment_author_email', 'amendment_author_org', 'amendment_comment',  # noqa
]


class Command(BaseCommand):
    """
    This command will generate 2 Table Schemas of the Aid model:
    - one with the english field names & choices values
    - another with the french field verbose_names & choices translated values

    Schema ? see aids/schema/README.md

    Usage
    python manage.py generate_aids_table_schema
    """

    def handle(self, *args, **options):
        self.generate_aids_schema()
        self.generate_aids_schema(use_french=True)

    def generate_aids_schema(self, use_french=False):
        schema = copy.deepcopy(SCHEMA_BASE)

        for field in (Aid._meta.model._meta.fields + Aid._meta.model._meta.many_to_many):
            field_column_name = field.column_name if hasattr(field, 'column_name') else field.name

            if field_column_name not in EXCLUDED_FIELDS:
                field_dict = dict()

                field_verbose_name = field.verbose_name
                field_dict['name'] = field_verbose_name if use_french else field_column_name
                field_dict['title'] = field_column_name if use_french else field_verbose_name

                field_dict['description'] = field.help_text
                # field['example'] = 

                field_dict['type'] = TYPE_MAPPING.get(type(field))
                if type(field) in STRING_FORMAT_MAPPING.keys():
                    field_dict['format'] = STRING_FORMAT_MAPPING.get(type(field))

                field_dict['constraints'] = dict()
                field_dict['constraints']['required'] = False

                if field.choices:
                    """
                    fields with 1 possible value (CharField + choices)
                    """
                    field_choices_list = [id for (id, name) in field.choices]
                    field_choices_verbose_list = [name for (id, name) in field.choices]
                    field_dict['constraints']['enum'] = field_choices_verbose_list if use_french else field_choices_list
                elif hasattr(field, 'base_field') and field.base_field.choices:
                    """
                    fields with 0, 1 or multiple possible values (ChoiceArrayField)
                    """
                    field_choices_list = [id for (id, name) in iter(dict(field.base_field.flatchoices).items())]
                    field_choices_verbose_list = [name for (id, name) in iter(dict(field.base_field.flatchoices).items())]
                    field_choices_pattern_list = field_choices_verbose_list if use_french else field_choices_list
                    field_choices_pattern_string = '|'.join(field_choices_pattern_list)
                    field_dict['constraints']['pattern'] = f'(?:(?:^|,)({field_choices_pattern_string}))+$'

                if type(field) == BooleanField:
                    field_dict['trueValues'] = BOOLEAN_TRUE_VALUES
                    field_dict['falseValues'] = BOOLEAN_FALSE_VALUES

                schema['fields'].append(field_dict)

        schema_file_path = os.path.join(os.getcwd(), SCHEMA_PATH_FRENCH if use_french else SCHEMA_PATH)
        with open(schema_file_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, ensure_ascii=False, indent=4)
