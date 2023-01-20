# Generated by Django 4.1.5 on 2023-01-19 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geofr", "0041_perimeter_population"),
    ]

    operations = [
        migrations.AddField(
            model_name="perimeter",
            name="projects_count",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="nombre de projets subventionnés"
            ),
        ),
    ]