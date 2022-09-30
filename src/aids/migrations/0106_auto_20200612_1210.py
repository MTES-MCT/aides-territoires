# Generated by Django 2.2.13 on 2020-06-12 10:10

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0105_remove_lessor_option"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aid",
            name="targeted_audiances",
            field=core.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("commune", "Communes"),
                        ("epci", "Audiance EPCI"),
                        ("unions", "Intermunicipal unions"),
                        ("department", "Departments"),
                        ("region", "Regions"),
                        ("association", "Associations"),
                        ("private_sector", "Private sector"),
                        ("public_cies", "Local public companies"),
                        ("public_org", "Public organization"),
                        ("researcher", "Research"),
                        ("private_person", "Individuals"),
                        ("farmer", "Farmers"),
                        ("other", "Other"),
                    ],
                    max_length=32,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="Targeted audiances",
            ),
        ),
    ]
