# Generated by Django 3.2.14 on 2022-08-30 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_translate_verbose_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-id'], 'verbose_name': 'projet', 'verbose_name_plural': 'projets'},
        ),
    ]
