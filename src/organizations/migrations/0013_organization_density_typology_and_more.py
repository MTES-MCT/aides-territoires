# Generated by Django 4.1.7 on 2023-03-30 14:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import geofr.services.validators


class Migration(migrations.Migration):

    dependencies = [
        ("backers", "0015_backer_perimeter"),
        ("organizations", "0012_organization_backer"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="density_typology",
            field=models.CharField(
                blank=True,
                help_text="définit le statut d’une commune rurale ou urbaine",
                max_length=50,
                verbose_name="Typologie",
            ),
        ),
        migrations.AddField(
            model_name="organization",
            name="insee_code",
            field=models.CharField(
                blank=True,
                help_text="Identifiant officiel défini dans le Code officiel géographique",
                max_length=5,
                null=True,
                verbose_name="code Insee",
            ),
        ),
        migrations.AddField(
            model_name="organization",
            name="population_strata",
            field=models.CharField(
                blank=True,
                choices=[
                    ("500-", "communes de 0 à 499 habitants"),
                    ("500_599", "communes de 500 à 999 habitants"),
                    ("1000_1999", "communes de 1\xa0000 à 1\xa0999 habitants"),
                    ("2000_3499", "communes de 2\xa0000 à 3\xa0499 habitants"),
                    ("3500_4999", "communes de 3\xa0500 à 4\xa0999 habitants"),
                    ("5000_7499", "communes de 5\xa0000 à 7\xa0499 habitants"),
                    ("7500_9999", "communes de 7\xa0500 à 9\xa0999 habitants"),
                    ("10000_14999", "communes de 10\xa0000 à 14\xa0999 habitants"),
                    ("15000_19999", "communes de 15\xa0000 à 19\xa0999 habitants"),
                    ("20000_34999", "communes de 20\xa0000 à 34\xa0999 habitants"),
                    ("35000_49999", "communes de 35\xa0000 à 49\xa0999 habitants"),
                    ("50000_74999", "communes de 50\xa0000 à 74\xa0999 habitants"),
                    ("75000_99999", "communes de 75\xa0000 à 99\xa0999 habitants"),
                    ("100000_199999", "communes de 100\xa0000 à 199\xa0999 habitants"),
                    ("200000+", "communes de 200\xa0000 habitants et plus"),
                ],
                max_length=15,
                null=True,
                verbose_name="Strate démographique",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="ape_code",
            field=models.CharField(
                blank=True,
                max_length=5,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9]{2}\\.?[0-9]{2}[a-zA-Z]{1}$"
                    )
                ],
                verbose_name="Code APE",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="backer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="backers.backer",
                verbose_name="Porteur d’aides",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="running_track_number",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Nombre de pistes d’athlétisme"
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="siren_code",
            field=models.CharField(
                blank=True,
                help_text="Identifiant officiel à 9 chiffres défini dans la base SIREN",
                max_length=9,
                null=True,
                validators=[geofr.services.validators.validate_siren],
                verbose_name="numéro Siren",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="siret_code",
            field=models.CharField(
                blank=True,
                help_text="Identifiant officiel à 14 chiffres défini dans la base SIREN",
                max_length=14,
                null=True,
                validators=[geofr.services.validators.validate_siret],
                verbose_name="numéro Siret",
            ),
        ),
    ]
