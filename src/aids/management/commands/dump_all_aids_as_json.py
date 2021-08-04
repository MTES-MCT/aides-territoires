from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.core.management.base import BaseCommand


from rest_framework.renderers import JSONRenderer

from aids.api.serializers import AidSerializerLatest
from aids.models import Aid


class Command(BaseCommand):
    """Dumps all aids as json file."""

    def handle(self, *args, **options):
        qs = Aid.objects.live()
        serializer = AidSerializerLatest(qs, many=True)
        json_data = JSONRenderer().render(serializer.data)
        file_obj = ContentFile(json_data)
        storage.save(settings.ALL_AIDS_DUMP_FILE_PATH, file_obj)
