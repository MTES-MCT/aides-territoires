# Generated by Django 2.2.16 on 2020-12-04 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backers", "0007_auto_20201203_1303"),
    ]

    operations = [
        migrations.AddField(
            model_name="backer",
            name="description",
            field=models.TextField(
                default="", verbose_name="Full description of the backer"
            ),
        ),
    ]
