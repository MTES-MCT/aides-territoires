# Generated by Django 2.2.13 on 2020-06-12 09:50

from django.db import migrations


def remove_lessor_option(apps, schema_editor):
    Aid = apps.get_model("aids", "Aid")
    aids = Aid.objects.filter(targeted_audiances__overlap=["lessor"])

    for aid in aids:
        aid.targeted_audiances.append("public_cies")
        aid.targeted_audiances.remove("lessor")
        aid.save()


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0104_auto_20200421_1209"),
    ]

    operations = [migrations.RunPython(remove_lessor_option)]
