from django.core import management
import logging


from core.celery import app
logger = logging.getLogger(__name__)


@app.task
def task_import_ademe():
    """Import data from the Ademe data feed."""
    logger.info('Starting ADEME import task')
    management.call_command('import_ademe', verbosity=1)


@app.task
def task_send_alerts():
    """Send an email alert upon new aid results."""
    logger.info('Starting alert sending tasks')
    management.call_command('send_alerts', verbosity=1)


@app.task
def task_export_contacts():
    """Export all accounts to the newsletter provider"""
    logger.info('Starting export contact tasks')
    management.call_command('export_contacts', verbosity=1)
