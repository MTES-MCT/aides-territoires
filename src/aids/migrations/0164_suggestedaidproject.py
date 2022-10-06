# Generated by Django 3.2.15 on 2022-09-29 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0012_alter_project_options"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("aids", "0163_alter_aidproject_creator"),
    ]

    operations = [
        migrations.CreateModel(
            name="SuggestedAidProject",
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
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Date de création",
                    ),
                ),
                (
                    "aid",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aids.aid",
                        verbose_name="Aide suggérée",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Créateur",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                        verbose_name="Projet",
                    ),
                ),
            ],
        ),
    ]
