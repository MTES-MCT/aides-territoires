# Generated by Django 2.2.16 on 2020-10-30 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0021_auto_20201030_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchpage',
            old_name='available_perimeter',
            new_name='available_perimeters',
        ),
    ]
