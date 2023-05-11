from io import BytesIO
import os
from openpyxl import Workbook
from xhtml2pdf import pisa
from datetime import date, datetime

from django.http import HttpResponse
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.utils.text import get_valid_filename

from aids.resources import AidResourcePublic
from aids.models import Aid
from organizations.models import Organization


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


def export_aids(organization, file_format: str) -> dict:
    organization = Organization.objects.get(pk=organization)
    users = organization.beneficiaries.values_list("pk", flat=True)
    aids_qs = Aid.objects.live().filter(author__in=users)

    exported_aids = AidResourcePublic().export(aids_qs)

    today = date.today()
    today_formated = today.strftime("%Y-%m-%d")

    filename = get_valid_filename(
        f"Aides-territoires - {today_formated } - {organization.name}.{file_format}"
    )

    if file_format == "csv":
        response = {
            "content": exported_aids.csv.encode(),
            "content_type": "text/csv",
            "filename": filename,
        }
    elif file_format == "xlsx":
        exported_aids.title = "Aides-territoires"  # Sheet title
        response = {
            "content": exported_aids.xlsx,
            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "filename": filename,
        }
    elif file_format == "pdf":
        template = get_template("aids/aids_export_pdf.html")

        current_site = Site.objects.get_current()
        html = template.render(
            {
                "today": today,
                "organization": organization,
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


def export_aid_stats(
    aid,
    start_date,
    end_date,
    view_events,
    application_url_click_events_count,
    private_projects_linked_count,
    public_projects_linked_count,
) -> dict:

    today = date.today()
    today_formated = today.strftime("%d-%m-%Y")

    if end_date is None:
        end_date_formated = today_formated
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        end_date_formated = end_date.strftime("%d-%m-%Y")

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_date_formated = start_date.strftime("%d-%m-%Y")

    aid_name = aid.name
    period = f"du {start_date_formated} au {end_date_formated}"
    view_events = str(view_events)
    application_url_click_events_count = str(application_url_click_events_count)
    private_projects_linked_count = str(private_projects_linked_count)
    public_projects_linked_count = str(public_projects_linked_count)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = "attachment; filename=Aides-territoires-{today_formated}-{aid_name}.xlsx".format(
        today_formated=today_formated, aid_name=aid_name
    )

    workbook = Workbook()

    # Get active worksheet/tab
    worksheet = workbook.active
    worksheet.title = f"Aides-territoires-statistiques-{today_formated}"

    # Define the titles for columns
    columns = [
        "Période choisie",
        "Nom de l'aide",
        "Nombre de vues",
        "Nombre de clics sur Candidater",
        "Nombre de projets privés liés",
        "Nombre de projets publics liés",
    ]
    row_num = 1

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    row_num += 1
    # Define the data for each cell in the row
    row = [
        period,
        aid_name,
        view_events,
        application_url_click_events_count,
        private_projects_linked_count,
        public_projects_linked_count,
    ]

    # Assign the data for each cell of the row
    for col_num, cell_value in enumerate(row, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = cell_value

    workbook.save(response)

    return response
