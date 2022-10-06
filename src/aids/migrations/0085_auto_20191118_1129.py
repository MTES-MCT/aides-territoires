# Generated by Django 2.2.7 on 2019-11-18 10:29

import core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0084_auto_20191107_1027"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aid",
            name="subvention_rate",
            field=core.fields.PercentRangeField(
                blank=True,
                help_text="If fixed rate, only fill the max. rate.",
                null=True,
                verbose_name="Subvention rate, min. and max. (in round %)",
            ),
        ),
    ]
