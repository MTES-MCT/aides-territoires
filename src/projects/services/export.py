from django.http import HttpResponse
from projects.models import Project

from aids.resources import AidResource


def export_project(project: Project, file_format: str) -> dict:
    aids_qs = project.aid_set.all()

    exported_aids = AidResource().export(aids_qs)

    print(exported_aids)

    filename = f"at-export-projet-{project.slug}.{file_format}"

    if file_format == "csv":
        response = {
            "content": exported_aids.csv.encode(),
            "content_type": "text/csv",
            "filename": filename,
        }
    elif file_format == "xlsx":
        response = {
            "content": exported_aids.xlsx,
            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "filename": filename,
        }

    else:
        response = {"error": "Unknown export format"}

    return response
