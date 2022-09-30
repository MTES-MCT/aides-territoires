# Generated by Django 3.1.5 on 2021-02-03 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0117_auto_20201211_1520"),
    ]

    operations = [
        migrations.AddField(
            model_name="aid",
            name="generic_aid",
            field=models.ForeignKey(
                help_text="Generic aid associated to a local aid",
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="local_aids",
                to="aids.aid",
                verbose_name="Generic aid",
            ),
        ),
    ]
