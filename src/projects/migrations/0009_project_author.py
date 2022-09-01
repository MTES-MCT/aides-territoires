# Generated by Django 3.2.6 on 2021-09-30 20:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0008_project_organizations"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="author",
            field=models.ManyToManyField(
                blank=True, to=settings.AUTH_USER_MODEL, verbose_name="Auteur"
            ),
        ),
    ]
