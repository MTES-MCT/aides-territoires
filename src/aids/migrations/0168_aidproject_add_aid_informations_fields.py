# Generated by Django 3.2.15 on 2022-10-14 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aids', '0167_suggestedaidproject_is_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='aidproject',
            name='aid_denied',
            field=models.BooleanField(default=False, help_text='Cette aide a-t-elle été refusée au porteur du projet ?', verbose_name='Aide refusée ?'),
        ),
        migrations.AddField(
            model_name='aidproject',
            name='aid_obtained',
            field=models.BooleanField(default=False, help_text='Cette aide a-t-elle été obtenue par le porteur du projet ?', verbose_name='Aide obtenue ?'),
        ),
        migrations.AddField(
            model_name='aidproject',
            name='aid_requested',
            field=models.BooleanField(default=False, help_text='Cette aide a-t-elle été demandée par le porteur du projet ?', verbose_name='Aide demandée ?'),
        ),
        migrations.AddField(
            model_name='aidproject',
            name='date_denied',
            field=models.DateTimeField(blank=True, help_text='Date à laquelle cette aide a été refusée au porteur du projet', null=True, verbose_name='Date du refus'),
        ),
        migrations.AddField(
            model_name='aidproject',
            name='date_obtained',
            field=models.DateTimeField(blank=True, help_text='Date à laquelle cette aide a été obtenue par le porteur du projet', null=True, verbose_name="Date de l'obtention"),
        ),
        migrations.AddField(
            model_name='aidproject',
            name='date_requested',
            field=models.DateTimeField(blank=True, help_text='Date à laquelle cette aide a été demandée par le porteur du projet', null=True, verbose_name='Date de la demande'),
        ),
    ]
