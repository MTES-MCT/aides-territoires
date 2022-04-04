from core.celery import app

from django.core import management


@app.task
def count_by_department():
    """Count backers and programs by department."""
    management.call_command("count_by_department")
