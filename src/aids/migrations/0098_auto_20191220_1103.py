# Generated by Django 2.2.8 on 2019-12-20 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0097_merge_20191220_1103"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aid",
            name="is_call_for_project",
            field=models.BooleanField(
                null=True,
                verbose_name="Call for project / Call for expressions of interest",
            ),
        ),
    ]
