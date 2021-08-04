from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from rest_framework.renderers import JSONRenderer

from aids.api.serializers import AidSerializerLatest
from aids.models import Aid

from storages.backends.s3boto3 import S3Boto3Storage


class Command(BaseCommand):
    """Dumps all aids as json file."""

    def handle(self, *args, **options):
        qs = Aid.objects.live()
        serializer = AidSerializerLatest(qs, many=True)
        json_data = JSONRenderer().render(serializer.data)
        storage = S3Boto3Storage(
            bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )
        import ipdb ; ipdb.set_trace()
        file_obj = ContentFile(json_data)
        storage.save(settings.ALL_AIDS_DUMP_FILE_PATH, file_obj)
