# Generated by Django 3.2.6 on 2021-08-20 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20210430_1323'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geofr', '0034_cleanup_choices_translations'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='beneficiaries',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Bénéficiaires'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='perimeter',
            field=models.ForeignKey(blank=True, help_text='Sur quel périmètre la structure intervient-elle ?', null=True, on_delete=django.db.models.deletion.PROTECT, to='geofr.perimeter', verbose_name='Périmètre de la structure'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='projects',
            field=models.ManyToManyField(blank=True, to='projects.Project', verbose_name='Projets'),
        ),
    ]