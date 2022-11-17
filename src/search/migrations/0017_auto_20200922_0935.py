# Generated by Django 2.2.16 on 2020-09-22 07:35

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0016_merge_20200922_0934"),
    ]

    operations = [
        migrations.RenameField(
            model_name="searchpage",
            old_name="available_audiances",
            new_name="available_audiences",
        ),
        migrations.AlterField(
            model_name="searchpage",
            name="show_audience_field",
            field=models.BooleanField(
                default=True, verbose_name="Show audience field?"
            ),
        ),
    ]
