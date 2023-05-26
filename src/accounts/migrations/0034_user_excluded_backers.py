# Generated by Django 4.2.1 on 2023-05-25 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backers", "0016_alter_backer_options_alter_backergroup_options_and_more"),
        ("accounts", "0033_user_notification_counter_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="excluded_backers",
            field=models.ManyToManyField(
                blank=True, to="backers.backer", verbose_name="Porteurs d’aides masqués"
            ),
        ),
    ]
