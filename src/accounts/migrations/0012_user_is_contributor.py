# Generated by Django 3.2.2 on 2021-05-18 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0011_auto_20210208_1628"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_contributor",
            field=models.BooleanField(
                default=True,
                help_text="Can access a dashboard to create aids",
                verbose_name="Is contributor",
            ),
        ),
    ]
