import re

from django.apps import apps
from django.db.models import TextField
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage

from django.conf import settings


class Command(BaseCommand):
    """Update media urls in Rich text fields to s3."""

    def handle(self, *args, **options):
        # Fetch ALL models, and for each model…
        models = apps.get_models()
        for model in models:

            # …check every rich text field
            fields = model._meta.get_fields()
            for field in fields:
                if isinstance(field, TextField):
                    self.stdout.write(f"Updating {model} {field.name}")
                    self.update_urls(model, field.name)

    def update_urls(self, Model, field_name):
        """For a given model and field, rewrite media urls."""

        items = Model.objects.filter(**{f"{field_name}__contains": 'src="/media/'})
        for item in items:
            value = getattr(item, field_name)
            urls = re.findall('src="/media/([^"]+)"', value)
            for url in urls:

                new_url = default_storage.url(f"{settings.MEDIA_ROOT}/{url}")
                value = value.replace(f"/media/{url}", new_url)
                self.stdout.write(f"    Updating {item} #{item.pk}: {url} => {new_url}")
            setattr(item, field_name, value)
            item.save()
