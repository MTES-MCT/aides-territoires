# Generated by Django 3.2.14 on 2022-08-19 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_auto_20220809_1456'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': 'Utilisateur', 'verbose_name_plural': 'Utilisateurs'},
        ),
    ]
