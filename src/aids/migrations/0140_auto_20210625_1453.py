# Generated by Django 3.2.4 on 2021-06-25 12:53

# This migration used the now removed tags app
# and has been edited to remove reference to it.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0139_auto_20210616_1335"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aid",
            name="tags",
        ),
    ]
