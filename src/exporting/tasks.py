from django.core import files
from django.core.files.base import ContentFile
from django.utils import timezone, dateformat

from core.celery import app

from aids.models import Aid
from aids.resources import AidResource
from exporting.models import DataExport


def export_aids(aids_id_list, author_id, file_format):
    queryset = Aid.objects.filter(id__in=aids_id_list)
    exported_data = AidResource().export(queryset)
    if file_format == 'csv':
        content_file = ContentFile(exported_data.csv.encode())
    if file_format == 'xlsx':
        content_file = ContentFile(exported_data.xlsx)
    file_name = 'export-aides-'
    file_name += dateformat.format(timezone.now(), 'Y-m-d_H-i-s')
    file_name += f'.{file_format}'
    file_object = files.File(content_file, name=file_name)
    DataExport.objects.create(
        author_id=author_id,
        exported_file=file_object,
    )
    file_object.close()
    content_file.close()


@app.task
def export_aids_as_csv(aids_id_list, author_id):
    export_aids(aids_id_list, author_id, file_format='csv')


@app.task
def export_aids_as_xlsx(aids_id_list, author_id):
    export_aids(aids_id_list, author_id, file_format='xlsx')
