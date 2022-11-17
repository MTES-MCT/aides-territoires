# Generated by Django 2.2.16 on 2020-12-08 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DataExport",
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
                    "exported_file",
                    models.FileField(
                        upload_to="data-export", verbose_name="exported file"
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date created"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="The person who has trigger the export",
                        limit_choices_to={"is_superuser": True},
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Data export",
                "verbose_name_plural": "Data export",
            },
        ),
    ]
