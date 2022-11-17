# Generated by Django 2.2.13 on 2020-09-07 07:33

from django.db import migrations, models
import search.models


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0011_searchpage_meta_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchpage",
            name="show_audiance_field",
            field=models.BooleanField(
                default=True, verbose_name="Show audiance field?"
            ),
        ),
        migrations.AddField(
            model_name="searchpage",
            name="show_categories_field",
            field=models.BooleanField(
                default=True, verbose_name="Show categories field?"
            ),
        ),
        migrations.AddField(
            model_name="searchpage",
            name="show_perimeter_field",
            field=models.BooleanField(
                default=True, verbose_name="Show perimeter field?"
            ),
        ),
        migrations.AlterField(
            model_name="searchpage",
            name="meta_image",
            field=models.FileField(
                blank=True,
                help_text="Make sure the file is at least 1024px long.",
                null=True,
                upload_to=search.models.meta_upload_to,
                verbose_name="Meta image",
            ),
        ),
    ]
