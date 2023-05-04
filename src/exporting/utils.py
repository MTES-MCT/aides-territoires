from django.urls import reverse
from django.utils.safestring import mark_safe


def get_admin_export_message():
    url = reverse("admin:exporting_dataexport_changelist")
    msg = f'Les données exportées seront disponibles <a href="{url}"> ici : {url}</a>'
    return mark_safe(msg)  # nosec B308 B703
