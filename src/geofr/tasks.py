from django.core import management
from django.template.loader import render_to_string

from core.celery import app
from geofr.models import Perimeter
from geofr.utils import attach_perimeters
from accounts.models import User
from emails.utils import send_email

from django.conf import settings

@app.task
def count_by_department():
    """Count backers and programs by department."""
    management.call_command("count_by_department")

@app.task
def attach_perimeters_async(perimeter_id: int, city_codes: set, user_id: int):
    """Attach perimeters with delay."""
    adhoc_perimeter = Perimeter.objects.get(id=perimeter_id)
    attach_perimeters(adhoc_perimeter, city_codes)

    user = User.objects.get(id=user_id)
    body_template = "emails/import_perimeter_success.txt"
    login_email_body = render_to_string(body_template, {
        'user_name': user.full_name,
        'perimeter_name': adhoc_perimeter.name
    })

    send_email(
        subject="Définition de votre périmètre",
        body=login_email_body,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        tags=['périmètres', settings.ENV_NAME],
        fail_silently=False
    )
