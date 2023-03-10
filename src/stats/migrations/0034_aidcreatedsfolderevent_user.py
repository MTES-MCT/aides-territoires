# Generated by Django 4.1.5 on 2023-03-06 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("stats", "0033_contactformsendevent"),
    ]

    operations = [
        migrations.AddField(
            model_name="aidcreatedsfolderevent",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Utilisateur",
            ),
        ),
    ]
