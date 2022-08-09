# Generated by Django 2.2.13 on 2020-09-07 14:34

from django.db import migrations


def update_emails_to_lowercase(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    users = User.objects.all()
    for user in users:
        user.email = user.email.lower()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_auto_20190115_1127"),
    ]

    operations = [migrations.RunPython(update_emails_to_lowercase)]
