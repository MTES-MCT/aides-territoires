# Generated by Django 3.1.5 on 2021-02-18 10:49

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="status",
            field=django_xworkflows.models.StateField(
                max_length=16,
                verbose_name="Status",
                workflow=django_xworkflows.models._SerializedWorkflow(
                    initial_state="reviewable",
                    name="ProjectWorkflow",
                    states=["draft", "reviewable", "published"],
                ),
            ),
        ),
    ]
