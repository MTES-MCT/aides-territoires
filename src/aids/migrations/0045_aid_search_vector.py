# Generated by Django 2.1.2 on 2018-11-06 14:20

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0044_auto_20181029_1516"),
    ]

    operations = [
        migrations.AddField(
            model_name="aid",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(
                null=True, verbose_name="Search vector"
            ),
        ),
    ]
