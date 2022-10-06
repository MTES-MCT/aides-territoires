# Generated by Django 2.2.7 on 2019-11-29 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
        ("aids", "0092_auto_20191128_1646"),
    ]

    operations = [
        migrations.AddField(
            model_name="aid",
            name="categories",
            field=models.ManyToManyField(
                blank=True,
                related_name="aids",
                to="categories.Category",
                verbose_name="Category",
            ),
        ),
    ]
