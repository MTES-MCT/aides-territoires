# Generated by Django 3.2.6 on 2021-10-26 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_project_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name="Date d'échéance"),
        ),
    ]
