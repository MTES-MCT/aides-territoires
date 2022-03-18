from django.core import management

from core.celery import app


@app.task
def count_by_department():
    """Count backers and programs by department."""
    management.call_command("count_by_department")
