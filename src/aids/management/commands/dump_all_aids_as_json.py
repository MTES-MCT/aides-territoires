from urllib.parse import urljoin

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import timezone


from rest_framework.renderers import JSONRenderer

from aids.api.serializers import AidSerializerLatest
from aids.models import Aid
from core.utils import get_base_url


class Command(BaseCommand):
    """Dumps all aids as json file."""

    def handle(self, *args, **options):
        qs = Aid.objects.live()
        serializer = AidSerializerLatest(qs, many=True)
        aids_api_url = urljoin(get_base_url(), reverse('aids-list'))
        api_url = urljoin(get_base_url(), reverse('aids-all'))
        data = {
            'timestamp': timezone.now(),
            'api_url': api_url,
            'aids_api_url': aids_api_url,
            'count': qs.count(),
            'results': serializer.data,
        }
        json_data = JSONRenderer().render(data)
        file_obj = ContentFile(json_data)
        storage.save(settings.ALL_AIDS_DUMP_FILE_PATH, file_obj)
