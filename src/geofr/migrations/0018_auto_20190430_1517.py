# Generated by Django 2.2 on 2019-04-30 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geofr", "0017_auto_20190408_1435"),
    ]

    operations = [
        migrations.AlterField(
            model_name="perimeter",
            name="scale",
            field=models.PositiveIntegerField(
                choices=[
                    (1, "Commune"),
                    (5, "EPCI"),
                    (8, "Drainage basin"),
                    (10, "Department"),
                    (15, "Region"),
                    (16, "Overseas"),
                    (17, "Mainland"),
                    (20, "Country"),
                    (25, "Continent"),
                ],
                verbose_name="Scale",
            ),
        ),
    ]
