# Generated by Django 4.2.3 on 2023-08-07 08:50

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0179_aid_contact_info_updated_alter_aid_aid_types_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aid",
            name="destinations",
            field=core.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("supply", "Dépenses de fonctionnement"),
                        ("investment", "Dépenses d’investissement"),
                    ],
                    max_length=32,
                ),
                blank=True,
                help_text="Obligatoire pour les aides financières",
                null=True,
                size=None,
                verbose_name="Types de dépenses / actions couvertes",
            ),
        ),
    ]
