# Generated by Django 4.1.7 on 2023-05-09 14:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("aids", "0177_alter_aid_loan_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aid",
            name="application_url",
            field=models.URLField(
                blank=True, max_length=700, verbose_name="Candidater à l’aide"
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="origin_url",
            field=models.URLField(
                blank=True, max_length=700, verbose_name="Plus d’informations"
            ),
        ),
    ]