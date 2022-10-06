# Generated by Django 2.2.1 on 2019-06-25 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0065_set_first_publication_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="aid",
            name="amended_aid",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="aids.Aid",
                verbose_name="Amended aid",
            ),
        ),
        migrations.AddField(
            model_name="aid",
            name="is_amendment",
            field=models.BooleanField(default=False, verbose_name="Is amendment"),
        ),
    ]
