from django.apps import apps
from django.core.management.base import BaseCommand

from storages.backends.s3boto3 import S3Boto3Storage


class Command(BaseCommand):
    """Copy all files and images to a new S3 bucket."""

    def add_arguments(self, parser):
        parser.add_argument("new_bucket", type=str)
        parser.add_argument("endpoint", type=str)

    def get_storage(self, bucket_name, endpoint_url):
        """Creates a new S3 storage object."""

        # Note : other parameters will be fetched from settings
        storage = S3Boto3Storage(bucket_name=bucket_name, endpoint_url=endpoint_url)
        return storage

    def handle(self, *args, **options):
        """Copy ALL files to a new bucket."""

        # Get a storage object connected to a new bucket
        new_bucket = options["new_bucket"]
        endpoint = options["endpoint"]
        new_storage = self.get_storage(new_bucket, endpoint)

        # Fetch ALL models, and for each model…
        models = apps.get_models()
        for model in models:

            # …check every field for a storage object
            fields = model._meta.get_fields()
            for field in fields:

                # if there is a storage object, it means it's a media file
                if hasattr(field, "storage"):
                    self.stdout.write(f"Copying {model} {field.name}")
                    self.reupload_files(model, field.name, new_storage)

    def reupload_files(self, Model, field_name, new_storage):
        """For a given model and field, copy all files to new storage."""

        items = Model.objects.exclude(**{f"{field_name}__isnull": True}).exclude(
            **{field_name: ""}
        )

        for item in items:
            field = getattr(item, field_name)
            with field.open() as f:
                new_storage.save(field.name, f)
