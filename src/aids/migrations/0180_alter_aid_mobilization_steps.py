import core.fields
from django.db import migrations, models
from model_utils import Choices


def update_mobilization_steps_field(apps, schema_editor):

    STEPS = Choices(
        ("preop", "Réflexion / conception"),
        ("preop_strategy", "Émergence / stratégie"),
        ("preop_conception", "Conception / faisabilité"),
        ("op", "Exécution"),
        ("postop", "Suivi / évaluation"),
    )

    Aid = apps.get_model("aids.Aid")
    aids = Aid.objects.all()

    for aid in aids:
        if aid.mobilization_steps is not None:
            if STEPS.preop in aid.mobilization_steps:
                aid.mobilization_steps.append(STEPS.preop_strategy)
                aid.mobilization_steps.append(STEPS.preop_conception)
                aid.mobilization_steps.remove(STEPS.preop)
                aid.save()


class Migration(migrations.Migration):
    dependencies = [
        ("aids", "0179_aid_contact_info_updated_alter_aid_aid_types_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aid",
            name="mobilization_steps",
            field=core.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("preop", "Réflexion / conception"),
                        ("preop_strategy", "Émergence / stratégie"),
                        ("preop_conception", "Conception / faisabilité"),
                        ("op", "Exécution"),
                        ("postop", "Suivi / évaluation"),
                    ],
                    default="preop_strategy",
                    max_length=32,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="État d’avancement du projet pour bénéficier du dispositif",
            ),
        ),
        migrations.RunPython(
            update_mobilization_steps_field, reverse_code=migrations.RunPython.noop
        ),
    ]
