from io import BytesIO
import os
from xhtml2pdf import pisa

from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import get_template

from aids.resources import AidResource
from projects.models import Project


def fetch_resources(uri: str, rel) -> str:
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    static_url = settings.STATIC_URL  # Typically /static/
    static_root = settings.STATIC_ROOT  # Typically /some/path/project_static/
    media_url = settings.MEDIA_URL  # Typically /media/
    media_root = settings.MEDIA_ROOT  # Typically /some/path/project_static/media/

    if uri.startswith(media_url):
        path = os.path.join(media_root, uri.replace(media_url, ""))
    elif uri.startswith(static_url):
        path = os.path.join(static_root, uri.replace(static_url, ""))
    else:
        return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception("media URI must start with %s or %s" % (static_url, media_url))

    return path


def export_project(project: Project, file_format: str) -> dict:
    aids_qs = project.aid_set.all()

    exported_aids = AidResource().export(aids_qs)

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
    elif file_format == "pdf":
        template = get_template("projects/project_export_pdf.html")

        current_site = Site.objects.get_current()
        html = template.render(
            {
                "project": project,
                "aid_set": aids_qs,
                "hostname": f"https://{current_site.domain}",
            }
        )

        result = BytesIO()
        pdf = pisa.CreatePDF(
            BytesIO(html.encode("utf-8")), dest=result, link_callback=fetch_resources
        )

        if not pdf.err:
            response = {
                "content": result.getvalue(),
                "content_type": "application/pdf",
                "filename": filename,
            }
        else:
            response = {"error": "PDF generation error", "error_detail": pdf.err}

        result.close()
    else:
        response = {"error": "Unknown export format", "error_detail": file_format}

    return response
