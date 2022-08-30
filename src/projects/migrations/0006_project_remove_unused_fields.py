# Generated by Django 3.2.6 on 2021-09-21 12:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0005_auto_20210430_1323"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="categories",
        ),
        migrations.RemoveField(
            model_name="project",
            name="is_suggested",
        ),
        migrations.RemoveField(
            model_name="project",
            name="status",
        ),
    ]
