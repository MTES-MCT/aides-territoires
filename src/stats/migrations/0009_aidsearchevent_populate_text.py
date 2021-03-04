# Generated by Django 3.1.7 on 2021-03-02 18:37

from django.db import migrations

from search.utils import get_querystring_value_from_key


def populate_aidsearchevent_text(apps, schema_editor):
    AidSearchEvent = apps.get_model('stats', 'AidSearchEvent')
    for event in AidSearchEvent.objects.all():
        event.text = get_querystring_value_from_key(event.querystring, 'text')
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_aidsearchevent_text'),
    ]

    operations = [
        migrations.RunPython(populate_aidsearchevent_text)
    ]
