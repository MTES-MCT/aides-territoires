# Generated by Django 4.2.3 on 2023-08-04 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("upload", "0003_change_verbose_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uploadimage",
            name="uploaded_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Uploadé à"),
        ),
    ]