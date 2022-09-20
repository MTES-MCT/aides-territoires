# Generated by Django 2.1 on 2018-09-04 12:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Perimeter",
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
                    "scale",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "Commune"),
                            (2, "EPCI"),
                            (3, "Department"),
                            (4, "Region"),
                            (5, "Cluster"),
                            (6, "Country"),
                            (7, "Continent"),
                        ],
                        verbose_name="Scale",
                    ),
                ),
                ("code", models.CharField(max_length=16, verbose_name="Code")),
                ("name", models.CharField(max_length=128, verbose_name="Name")),
                (
                    "country",
                    models.CharField(
                        blank=True,
                        default="99100",
                        max_length=8,
                        verbose_name="Country",
                    ),
                ),
                (
                    "region",
                    models.CharField(blank=True, max_length=2, verbose_name="Region"),
                ),
                (
                    "department",
                    models.CharField(
                        blank=True, max_length=3, verbose_name="Departments"
                    ),
                ),
                (
                    "epci",
                    models.CharField(blank=True, max_length=32, verbose_name="EPCI"),
                ),
                (
                    "commune",
                    models.CharField(blank=True, max_length=32, verbose_name="Commune"),
                ),
                (
                    "zipcodes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=8),
                        blank=True,
                        null=True,
                        size=None,
                        verbose_name="Zip codes",
                    ),
                ),
            ],
            options={
                "verbose_name": "Perimeter",
                "verbose_name_plural": "Perimeters",
            },
        ),
    ]
