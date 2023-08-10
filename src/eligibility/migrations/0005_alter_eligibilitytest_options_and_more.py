# Generated by Django 4.2.3 on 2023-08-04 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("eligibility", "0004_eligibilitytest_conclusions"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eligibilitytest",
            options={
                "verbose_name": "Test d’éligibilité",
                "verbose_name_plural": "Tests d’éligibilité",
            },
        ),
        migrations.AlterField(
            model_name="eligibilityquestion",
            name="answer_choice_a",
            field=models.CharField(max_length=256, verbose_name="Réponse A"),
        ),
        migrations.AlterField(
            model_name="eligibilityquestion",
            name="answer_choice_b",
            field=models.CharField(max_length=256, verbose_name="Réponse B"),
        ),
        migrations.AlterField(
            model_name="eligibilityquestion",
            name="answer_choice_c",
            field=models.CharField(
                blank=True, max_length=256, verbose_name="Réponse C"
            ),
        ),
        migrations.AlterField(
            model_name="eligibilityquestion",
            name="answer_choice_d",
            field=models.CharField(
                blank=True, max_length=256, verbose_name="Réponse D"
            ),
        ),
        migrations.AlterField(
            model_name="eligibilityquestion",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="eligibility_questions",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Auteur",
            ),
        ),
        migrations.AlterField(
            model_name="eligibilityquestion",
            name="date_created",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Date de création"
            ),
        ),
        migrations.AlterField(
            model_name="eligibilityquestion",
            name="date_updated",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Date de mise à jour"
            ),
        ),
        migrations.AlterField(
            model_name="eligibilitytest",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="eligibility_tests",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Auteur",
            ),
        ),
        migrations.AlterField(
            model_name="eligibilitytest",
            name="date_created",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Date de création"
            ),
        ),
        migrations.AlterField(
            model_name="eligibilitytest",
            name="date_updated",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Date de mise à jour"
            ),
        ),
        migrations.AlterField(
            model_name="eligibilitytest",
            name="name",
            field=models.CharField(max_length=256, verbose_name="Nom"),
        ),
    ]