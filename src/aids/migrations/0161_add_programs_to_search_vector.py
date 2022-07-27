from django.db import migrations
from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import Value


def update_search_vector_unaccented(apps, schema_editor):
    Aid = apps.get_model("aids.Aid")
    aids = Aid.objects.all()
    for aid in aids:
        backers = aid.financers.all() | aid.instructors.all()
        categories = aid.categories.all()
        keywords = aid.keywords.all()
        programs = aid.programs.all()
        search_vector_unaccented = (
            SearchVector(
                Value(aid.name, output_field=models.CharField()),
                weight="A",
                config="french_unaccent",
            )
            + SearchVector(
                Value(aid.name_initial, output_field=models.CharField()),
                weight="A",
                config="french_unaccent",
            )
            + SearchVector(
                Value(aid.short_title, output_field=models.CharField()),
                weight="A",
                config="french_unaccent",
            )
            + SearchVector(
                Value(
                    " ".join(str(category.name) for category in categories),
                    output_field=models.CharField(),
                ),
                weight="A",
                config="french_unaccent",
            )
            + SearchVector(
                Value(
                    " ".join(str(program.name) for program in programs),
                    output_field=models.CharField(),
                ),
                weight="A",
                config="french_unaccent",
            )
            + SearchVector(
                Value(
                    " ".join(str(keyword.name) for keyword in keywords),
                    output_field=models.CharField(),
                ),
                weight="C",
                config="french_unaccent",
            )
            + SearchVector(
                Value(aid.description, output_field=models.CharField()),
                weight="B",
                config="french_unaccent",
            )
            + SearchVector(
                Value(aid.project_examples, output_field=models.CharField()),
                weight="D",
                config="french_unaccent",
            )
            + SearchVector(
                Value(aid.eligibility, output_field=models.CharField()),
                weight="D",
                config="french_unaccent",
            )
            + SearchVector(
                Value(
                    " ".join(str(backer.name) for backer in backers),
                    output_field=models.CharField(),
                ),
                weight="D",
                config="french_unaccent",
            )
        )
        aid.search_vector_unaccented = search_vector_unaccented
        aid.save()


class Migration(migrations.Migration):

    dependencies = [
        ("aids", "0160_aid_import_data_mention"),
    ]

    operations = [
        migrations.RunPython(
            update_search_vector_unaccented, reverse_code=migrations.RunPython.noop
        )
    ]
