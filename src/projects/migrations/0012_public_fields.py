# Generated by Django 3.2.15 on 2022-09-19 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywords', '0002_synonymlist_model'),
        ('projects', '0011_translate_verbose_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='Ce projet est-il public?'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_types',
            field=models.ManyToManyField(blank=True, related_name='projects', to='keywords.SynonymList', verbose_name='Types de projet'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_types_suggestion',
            field=models.CharField(blank=True, max_length=256, verbose_name='Type de projet suggéré'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('draft', 'Brouillon'), ('reviewable', 'En revu'), ('published', 'Publié'), ('deleted', 'Supprimé')], default='draft', max_length=10, verbose_name='Statut'),
        ),
    ]