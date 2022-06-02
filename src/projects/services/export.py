import csv

from django.http import HttpResponse
from aids.api.serializers import AidSerializerLatest
from projects.models import Project


def csv_export_content(project: Project):
    aids = project.aid_set.all()
    fields = AidSerializerLatest.Meta.fields
    filename = f"{project.slug}.csv"
    print(aids, filename)

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

    writer = csv.writer(response)
    writer.writerow(fields)
    for aid in aids:
        serializer = AidSerializerLatest()
        formated_aid = serializer.get_object(aid)
        row = []
        for field in fields:
            row.append(getattr(formated_aid, field))

    return response
