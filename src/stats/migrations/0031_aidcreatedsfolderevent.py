# Generated by Django 4.1.5 on 2023-02-20 13:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0009_organization_imported_date_organization_is_imported"),
        ("aids", "0175_aid_ds_id_aid_ds_mapping_aid_ds_schema_exists"),
        ("stats", "0030_alter_aidoriginurlclickevent_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="AidCreateDSFolderEvent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ds_folder_url",
                    models.URLField(max_length=500, verbose_name="Url du dossier"),
                ),
                (
                    "ds_folder_id",
                    models.CharField(
                        help_text="ID du dossier en base 64",
                        max_length=200,
                        verbose_name="ID du dossier",
                    ),
                ),
                (
                    "ds_folder_number",
                    models.PositiveIntegerField(
                        help_text="ID du dossier en tant qu'entier",
                        verbose_name="Numéro du dossier",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Date de création",
                    ),
                ),
                (
                    "aid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="aids.aid",
                        verbose_name="Aide",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="organizations.organization",
                        verbose_name="Structure",
                    ),
                ),
            ],
            options={
                "verbose_name": "Événement création dossier Démarches-Simplifiées",
                "verbose_name_plural": "Événements création dossier Démarches-Simplifiées",
            },
        ),
    ]
