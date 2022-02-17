from django.db import migrations
from django.contrib.postgres.search import SearchVector
from django.db.models import Value


def update_search_vector_unaccentedr(apps, schema_editor):
    Aid = apps.get_model('aids.Aid')
    aids = Aid.objects.all()
    for aid in aids:
        backers = aid.financers.all() | aid.instructors.all()
        categories = aid.categories.all()
        search_vector_unaccented = \
            SearchVector(Value(aid.name), weight='A', config='french_unaccent') + \
            SearchVector(Value(aid.name_initial, weight='A', config='french_unaccent') + \
            SearchVector(Value(aid.description), weight='B', config='french_unaccent') + \
            SearchVector(Value(aid.project_examples, weight='B', config='french_unaccent') + \
            SearchVector(Value(aid.eligibility), weight='D', config='french_unaccent') + \
            SearchVector(Value(' '.join(backer.name for backer in backers)), weight='D', config='french_unaccent') + \
            SearchVector(Value(' '.join(category.name for category in categories)), weight='D', config='french_unaccent')
        aid.search_vector_unaccented = search_vector_unaccented
        aid.save()

class Migration(migrations.Migration):

    dependencies = [
            ('aids', '0151_aid_author_notification'),
    ]

    operations = [
        migrations.RunPython(update_search_vector_unaccented, reverse_code=migrations.RunPython.noop)
    ]
