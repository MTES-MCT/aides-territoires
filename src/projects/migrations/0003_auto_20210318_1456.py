# Generated by Django 3.1.7 on 2021-03-18 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(db_index=True, max_length=256, verbose_name='Project name'),
        ),
    ]
