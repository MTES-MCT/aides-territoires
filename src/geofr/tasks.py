from django.core import management

from core.celery import app
from geofr.utils import attach_perimeters


@app.task
def count_by_department():
    """Count backers and programs by department."""
    management.call_command("count_by_department")

@app.task
def attach_perimeters_async(adhoc, city_codes, request):
    """Attach perimeters with delay."""
    attach_perimeters(adhoc, city_codes)
    user_email = request.user.email