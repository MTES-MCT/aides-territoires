# Generated by Django 2.1.5 on 2019-01-25 09:36

from django.db import migrations
from django.contrib.postgres.search import SearchVector
from django.db.models import Value

dependencies = [
]


def update_search_vector_unaccented(apps, schema_editor):
    Aid = apps.get_model('aids.Aid')
    aids = Aid.objects.all()
    for aid in aids:
        backers = aid.financers.all() | aid.instructors.all()
        search_vector_unaccented = \
            SearchVector(Value(aid.name), weight='A', config='french_unaccent') + \
            SearchVector(Value(aid.description), weight='B', config='french_unaccent') + \
            SearchVector(Value(aid.eligibility), weight='D', config='french_unaccent') + \
            SearchVector(Value(' '.join(backer.name for backer in backers)), weight='D', config='french_unaccent')
        aid.search_vector_unaccented = search_vector_unaccented
        aid.save()


class Migration(migrations.Migration):

    dependencies = [
        ('aids', '0141_aid_search_vector_unaccented'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aid',
            name='search_vector',
        ),
        migrations.RunPython(update_search_vector_unaccented, reverse_code=migrations.RunPython.noop)
    ]
