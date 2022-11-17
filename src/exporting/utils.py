from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


def get_admin_export_message():
    url = reverse("admin:exporting_dataexport_changelist")
    msg = _(f"Exported data will be available " f'<a href="{url}">here: {url}</a>')
    return mark_safe(msg)  # nosec B308 B703
