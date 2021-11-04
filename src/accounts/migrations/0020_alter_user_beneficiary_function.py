# Generated by Django 3.2.6 on 2021-10-01 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_user_beneficiary_function'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='beneficiary_function',
            field=models.CharField(blank=True, choices=[('elected', 'Élu'), ('agent', 'Agent territorial'), ('other', 'Autre')], max_length=32, null=True, verbose_name='Fonction du bénéficiaire'),
        ),
    ]
