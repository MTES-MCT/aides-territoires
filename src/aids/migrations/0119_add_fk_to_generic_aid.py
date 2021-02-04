# Generated by Django 3.1.5 on 2021-02-03 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aids', '0118_add_typology'),
    ]

    operations = [
        migrations.AddField(
            model_name='aid',
            name='generic_aid',
            field=models.ForeignKey(help_text='Generic aid associated to a local aid', limit_choices_to={'aid_typology': 'generic'}, null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='local_aids', to='aids.aid', verbose_name='Generic aid'),
        ),
    ]
