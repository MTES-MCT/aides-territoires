from django.http import HttpResponse
from projects.models import Project

from aids.resources import AidResource


def export_project(project: Project, file_format: str):
    aids_qs = project.aid_set.all()

    exported_aids = AidResource().export(aids_qs)

    print(exported_aids)

    filename = f"at-export-projet-{project.slug}.{file_format}"

    if file_format == "csv":
        response = HttpResponse(
            exported_aids.csv.encode(),
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    elif file_format == "xlsx":
        response = HttpResponse(
            exported_aids.xlsx,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    elif file_format == "pdf":
        pass
    else:
        # If file_format is not one of the above values, return a basic html page
        # Should only happen for debugging
        response = HttpResponse(
            f"Method: POST, project: {project.name}, format: {file_format}"
        )

    return response
