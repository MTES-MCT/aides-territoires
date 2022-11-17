# Generated by Django 3.2 on 2021-04-09 09:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0124_aid_eligibility_test"),
        ("eligibility", "0003_eligibilitytestquestion"),
        ("stats", "0016_aidmatchprojectevent"),
    ]

    operations = [
        migrations.CreateModel(
            name="AidEligibilityTestEvent",
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
                ("answer_success", models.BooleanField(null=True)),
                ("answer_details", models.JSONField(null=True)),
                (
                    "querystring",
                    models.TextField(default="", verbose_name="Querystring"),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True, default="", max_length=256, verbose_name="Source"
                    ),
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
                (
                    "eligibility_test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="eligibility.eligibilitytest",
                        verbose_name="Eligibility test",
                    ),
                ),
            ],
            options={
                "verbose_name": "Événement test d'éligibilité",
                "verbose_name_plural": "Événements tests d'éligibilité",
            },
        ),
    ]
