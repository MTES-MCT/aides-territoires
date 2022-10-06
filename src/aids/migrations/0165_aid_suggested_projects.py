# Generated by Django 3.2.15 on 2022-09-30 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0012_alter_project_options"),
        ("aids", "0164_suggestedaidproject"),
    ]

    operations = [
        migrations.AddField(
            model_name="aid",
            name="suggested_projects",
            field=models.ManyToManyField(
                blank=True,
                related_name="suggested_aid",
                through="aids.SuggestedAidProject",
                to="projects.Project",
                verbose_name="Projets suggérés",
            ),
        ),
    ]
