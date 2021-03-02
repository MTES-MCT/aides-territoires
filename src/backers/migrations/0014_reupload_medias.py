# Generated by Django 3.1.7 on 2021-02-23 13:08

from django.db import migrations
from django.db.migrations.operations.special import RunPython
from core.utils import reupload_files


class Migration(migrations.Migration):

    dependencies = [
        ('backers', '0013_fix_slug_length'),
    ]

    operations = [
        RunPython(reupload_files('backers.Backer', 'logo'), RunPython.noop)
    ]
