# Generated by Django 4.1.5 on 2023-02-23 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("organizations", "0009_organization_imported_date_organization_is_imported"),
        ("stats", "0030_alter_aidoriginurlclickevent_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="aidviewevent",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="organizations.organization",
                verbose_name="Structure",
            ),
        ),
        migrations.AddField(
            model_name="aidviewevent",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Utilisateur",
            ),
        ),
    ]
