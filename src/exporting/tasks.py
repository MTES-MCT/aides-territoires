from django.core import files
from django.core.files.base import ContentFile
from django.utils import timezone, dateformat

from core.celery import app

from aids.models import Aid
from aids.resources import AidResource
from exporting.models import DataExport


def export_aids(queryset, author_id, file_format):
    exported_data = AidResource().export(queryset)
    if file_format == 'csv':
        file_content = ContentFile(exported_data.csv.encode())
    if file_format == 'xlsx':
        file_content = ContentFile(exported_data.xlsx)
    file_name = 'export-aides-'
    file_name += dateformat.format(timezone.now(), 'Y-m-d_H-i-s')
    file_name += f'.{file_format}'
    file_object = files.File(file_content, name=file_name)
    DataExport.objects.create(
        author_id=author_id,
        exported_file=file_object,
    )
    file_object.close()
    file_content.close()


@app.task
def export_aids_as_csv(aids_id_list, author_id):
    queryset = Aid.objects.filter(id__in=aids_id_list)
    export_aids(queryset, author_id, file_format='csv')


@app.task
def export_aids_as_xlsx(aids_id_list, author_id):
    queryset = Aid.objects.filter(id__in=aids_id_list)
    export_aids(queryset, author_id, file_format='xlsx')


@app.task
def export_published_aids_as_csv(author_id):
    queryset = Aid.objects.published()
    export_aids(queryset, author_id, file_format='csv')


@app.task
def export_published_aids_as_xlsx(author_id):
    queryset = Aid.objects.published()
    export_aids(queryset, author_id, file_format='xlsx')


@app.task
def export_live_aids_as_csv(author_id):
    queryset = Aid.objects.live()
    export_aids(queryset, author_id, file_format='csv')


@app.task
def export_live_aids_as_xlsx(author_id):
    queryset = Aid.objects.live()
    export_aids(queryset, author_id, file_format='xlsx')
