# Generated by Django 3.2.4 on 2021-07-02 07:43

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0142_update_search_vector_unaccented"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="aid",
            name="aids_aid_search__5120d8_gin",
        ),
        migrations.AddIndex(
            model_name="aid",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector_unaccented"], name="aids_aid_search__81172f_gin"
            ),
        ),
    ]
