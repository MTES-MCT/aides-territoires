# Generated by Django 2.2.1 on 2019-09-16 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0068_auto_20190916_1103"),
    ]

    operations = [
        migrations.AddField(
            model_name="aid",
            name="amendment_author",
            field=models.CharField(
                blank=True, max_length=256, verbose_name="Amendment author"
            ),
        ),
        migrations.AddField(
            model_name="aid",
            name="amendment_comment",
            field=models.TextField(blank=True, verbose_name="Amendment comment"),
        ),
    ]
