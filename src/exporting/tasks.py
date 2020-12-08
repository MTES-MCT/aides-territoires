from django.core import files
from django.core.files.base import ContentFile
from django.utils import timezone, dateformat

from core.celery import app

from aids.models import Aid
from aids.resources import AidResource
from exporting.models import DataExport


@app.task
def export_aids_as_csv(aids_id_list, author_id):
    queryset = Aid.objects.filter(id__in=aids_id_list)
    exported_data = AidResource().export(queryset)
    content_file = ContentFile(exported_data.csv)
    file_name = 'export-aides-'
    file_name += dateformat.format(timezone.now(), 'Y-m-d_H-i-s')
    file_name += '.csv'
    file_object = files.File(content_file, name=file_name)
    DataExport.objects.create(
        author_id=author_id,
        exported_file=file_object,
    )
    file_object.close()
    content_file.close()
