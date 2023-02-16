# Generated by Django 4.1.5 on 2023-02-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0174_alter_aid_options_alter_aid_application_url_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="aid",
            name="ds_id",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Identifiant de la démarche sur Démarches-Simplifiées",
                null=True,
                verbose_name="Identifiant de la démarche",
            ),
        ),
        migrations.AddField(
            model_name="aid",
            name="ds_mapping",
            field=models.JSONField(
                blank=True,
                help_text="Mapping JSON pour pré-remplissage sur Démarches-Simplifiées",
                null=True,
                verbose_name="Mapping JSON de la démarche",
            ),
        ),
        migrations.AddField(
            model_name="aid",
            name="ds_schema_exists",
            field=models.BooleanField(
                default=False,
                help_text="Un schéma pour l'api de pré-remplissage de Démarches-Simplifiées est-il renseigné ?",
                verbose_name="Schéma existant",
            ),
        ),
    ]
