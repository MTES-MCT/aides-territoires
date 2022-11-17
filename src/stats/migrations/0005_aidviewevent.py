# Generated by Django 3.1.6 on 2021-02-12 16:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0117_auto_20201211_1520"),
        ("stats", "0004_event_source"),
    ]

    operations = [
        migrations.CreateModel(
            name="AidViewEvent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("querystring", models.TextField(verbose_name="Querystring")),
                (
                    "source",
                    models.CharField(default="", max_length=256, verbose_name="Source"),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Date created"
                    ),
                ),
                (
                    "aid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="aids.aid",
                        verbose_name="Aid",
                    ),
                ),
            ],
            options={
                "verbose_name": "Aid View Event",
                "verbose_name_plural": "Aid View Events",
            },
        ),
    ]
