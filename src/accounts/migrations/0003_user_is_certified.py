# Generated by Django 2.1.2 on 2018-11-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_auto_20181109_1456"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_certified",
            field=models.BooleanField(default=False, verbose_name="Is certified"),
        ),
    ]
