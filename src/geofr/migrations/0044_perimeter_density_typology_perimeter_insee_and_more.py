# Generated by Django 4.1.7 on 2023-03-24 14:10

from django.db import migrations, models
import geofr.services.validators


class Migration(migrations.Migration):

    dependencies = [
        ("geofr", "0043_perimeter_projects_count_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="perimeter",
            name="density_typology",
            field=models.CharField(
                blank=True,
                help_text="définit le statut d'une commune rurale ou urbaine",
                max_length=50,
                verbose_name="typologie",
            ),
        ),
        migrations.AddField(
            model_name="perimeter",
            name="insee",
            field=models.CharField(
                blank=True,
                help_text="Identifiant officiel défini dans le Code officiel géographique",
                max_length=5,
                null=True,
                verbose_name="code Insee",
            ),
        ),
        migrations.AddField(
            model_name="perimeter",
            name="siren",
            field=models.CharField(
                blank=True,
                help_text="Identifiant officiel défini dans la base SIREN",
                max_length=9,
                null=True,
                validators=[geofr.services.validators.validate_siren],
                verbose_name="numéro Siren",
            ),
        ),
        migrations.AddField(
            model_name="perimeter",
            name="siret",
            field=models.CharField(
                blank=True,
                help_text="Identifiant officiel défini dans la base SIREN",
                max_length=14,
                null=True,
                validators=[geofr.services.validators.validate_siret],
                verbose_name="numéro Siret",
            ),
        ),
    ]