# Generated by Django 2.2.13 on 2020-06-11 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_searchpage_logo_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchpage',
            name='color_5',
            field=models.CharField(blank=True, help_text='Footer background color', max_length=10, verbose_name='Color 5'),
        ),
    ]
