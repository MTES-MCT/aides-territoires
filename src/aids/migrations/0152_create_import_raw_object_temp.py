# Generated by Django 3.2.12 on 2022-02-21 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aids', '0151_aid_author_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='aid',
            name='import_raw_object_calendar',
            field=models.JSONField(editable=False, null=True, verbose_name='Donnée JSON brute du calendrier'),
        ),
        migrations.AddField(
            model_name='aid',
            name='import_raw_object_temp',
            field=models.JSONField(editable=False, null=True, verbose_name='Donnée JSON brute temporaire'),
        ),
        migrations.AddField(
            model_name='aid',
            name='import_raw_object_temp_calendar',
            field=models.JSONField(editable=False, null=True, verbose_name='Donnée JSON brute temporaire du calendrier'),
        ),
    ]
