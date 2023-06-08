from io import BytesIO
import os
from openpyxl import Workbook
from xhtml2pdf import pisa
from datetime import date, datetime, timedelta

from django.http import HttpResponse
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.utils.text import get_valid_filename
from django.utils import timezone
from django.db.models import Count

from aids.resources import AidResourcePublic
from aids.models import Aid, AidProject
from organizations.models import Organization
from stats.models import (
    AidApplicationUrlClickEvent,
    AidOriginUrlClickEvent,
    AidViewEvent,
)


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
    aids_qs = Aid.objects.live().filter(author__in=users).order_by("pk")

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


def export_aid_detail_pdf(aid, user, organization):

    today = date.today()
    today_formated = today.strftime("%Y-%m-%d")

    filename = get_valid_filename(
        f"Aides-territoires - {today_formated } - {aid.name}.pdf"
    )

    template = get_template("aids/aid_export_pdf.html")

    current_site = Site.objects.get_current()
    html = template.render(
        {
            "today": today,
            "aid": aid,
            "organization": organization,
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

    return response


def date_range_list(start_date, end_date):
    # Return list of datetime.date objects (inclusive) between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date)
        curr_date += timedelta(days=1)
    return date_list


def export_aid_stats(
    aid,
    start_date,
    end_date,
) -> dict:

    if end_date is None:
        end_date = timezone.now().date()
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    date_list = date_range_list(start_date, end_date)

    aid_name = aid.name

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = "attachment; filename=Aides-territoires-statistiques.xlsx"

    workbook = Workbook()

    # Get active worksheet/tab
    worksheet = workbook.active
    worksheet.title = f"Aides-territoires-statistiques-{aid_name}"

    # Define the titles for columns
    columns = [
        "Date",
        "Nombre de vues",
        "Nombre de clics sur Candidater",
        "Nombre de clics sur Plus d’informations",
        "Nombre de projets privés liés",
        "Nombre de projets publics liés",
    ]
    row_num = 1

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    # Define the data for each cell in the row
    aidviewevent_qs = (
        AidViewEvent.objects.filter(aid=aid.id)
        .extra({"date_created": "date(date_created)"})
        .values("date_created")
        .annotate(view_count=Count("date_created", distinct=True))
    )

    aidapplicationurlclickevent_qs = (
        AidApplicationUrlClickEvent.objects.filter(aid=aid.id)
        .extra({"date_created": "date(date_created)"})
        .values("date_created")
        .annotate(click_count=Count("date_created", distinct=True))
    )

    aidoriginurlclickevent_qs = (
        AidOriginUrlClickEvent.objects.filter(aid=aid.id)
        .extra({"date_created": "date(date_created)"})
        .values("date_created")
        .annotate(click_count=Count("date_created", distinct=True))
    )

    private_projects_linked_qs = (
        AidProject.objects.filter(aid=aid.id, project__is_public=False)
        .extra({"date_created": "date(aids_aidproject.date_created)"})
        .values("date_created")
        .annotate(linked_count=Count("date_created", distinct=True))
    )

    public_projects_linked_qs = (
        AidProject.objects.filter(aid=aid.id, project__is_public=True)
        .extra({"date_created": "date(aids_aidproject.date_created)"})
        .values("date_created")
        .annotate(linked_count=Count("date_created", distinct=True))
    )

    for day in date_list:
        row_num += 1
        row = [
            day.strftime("%d-%m-%Y"),
        ]
        day = datetime.strftime(day, "%Y-%m-%d")

        viewevent = 0
        for x in aidviewevent_qs:
            if datetime.strftime(x["date_created"], "%Y-%m-%d") == day:
                viewevent = x["view_count"]
        row.append(viewevent)

        aidapplicationurlclickevent = 0
        for x in aidapplicationurlclickevent_qs:
            if datetime.strftime(x["date_created"], "%Y-%m-%d") == day:
                aidapplicationurlclickevent = x["click_count"]
        row.append(aidapplicationurlclickevent)

        aidoriginurlclickevent = 0
        for x in aidoriginurlclickevent_qs:
            if datetime.strftime(x["date_created"], "%Y-%m-%d") == day:
                aidoriginurlclickevent = x["click_count"]
        row.append(aidoriginurlclickevent)

        private_projects_linked = 0
        for x in private_projects_linked_qs:
            if datetime.strftime(x["date_created"], "%Y-%m-%d") == day:
                private_projects_linked = x["linked_count"]
        row.append(private_projects_linked)

        public_projects_linked = 0
        for x in public_projects_linked_qs:
            if datetime.strftime(x["date_created"], "%Y-%m-%d") == day:
                public_projects_linked = x["linked_count"]
        row.append(public_projects_linked)

        # Assign the data for each cell of the row
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    workbook.save(response)

    return response
