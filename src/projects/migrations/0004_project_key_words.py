# Generated by Django 3.1.8 on 2021-04-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210318_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='key_words',
            field=models.TextField(blank=True, default='', verbose_name='key words associated to the project'),
        ),
    ]
