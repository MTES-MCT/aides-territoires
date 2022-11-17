# Generated by Django 3.1.7 on 2021-03-04 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backers", "0014_reupload_medias"),
        ("stats", "0010_auto_20210305_1619"),
    ]

    operations = [
        migrations.AddField(
            model_name="aidsearchevent",
            name="backers",
            field=models.ManyToManyField(
                blank=True,
                related_name="aid_search_events",
                to="backers.Backer",
                verbose_name="Backers",
            ),
        ),
    ]
