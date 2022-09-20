# Generated by Django 3.2.6 on 2022-01-31 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0004_add_update_timestamps"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Auteur",
            ),
        ),
    ]
