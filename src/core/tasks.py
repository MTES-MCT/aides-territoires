import logging

from django.core import management

from core.celery import app


logger = logging.getLogger(__name__)


@app.task
def task_import_pays_de_la_loire():
    """Import data from the Pays de la Loire data feed."""
    logger.info("Starting Pays de la Loire import task")
    management.call_command("import_pays_de_la_loire", verbosity=1)


@app.task
def task_import_ademe():
    """Import data from the Ademe data feed."""
    logger.info("Starting ADEME import task")
    management.call_command("import_ademe", verbosity=1)


@app.task
def task_send_alerts():
    """Send an email alert upon new aid results."""
    logger.info("Starting alert sending tasks")
    management.call_command("send_alerts", verbosity=1)


@app.task
def task_export_contacts():
    """Export all accounts to the newsletter provider"""
    logger.info("Starting export contact tasks")
    management.call_command("export_contacts", verbosity=1)


@app.task
def task_scale_up_scalingo_review_apps():
    logger.info("Starting Scalingo Review Apps scaling task")
    management.call_command("scale_scalingo_review_apps", "up", verbosity=1)


@app.task
def task_scale_down_scalingo_review_apps():
    logger.info("Starting Scalingo Review Apps scaling task")
    management.call_command("scale_scalingo_review_apps", "down", verbosity=1)


@app.task
def task_import_ministere_de_la_culture():
    """Import data from the 'Ministère de la culture' data feed."""
    logger.info("Starting Ministère de la culture import task")
    management.call_command("import_ministere_de_la_culture", verbosity=1)


@app.task
def task_import_departement_drome():
    """Import data from the 'Département Drome' data feed."""
    logger.info("Starting Département Drome import task")
    management.call_command("import_departement_drome", verbosity=1)


@app.task
def task_import_welcome_europe():
    """Import data from the 'Welcome Europe' data feed."""
    logger.info("Starting Welcome Europe import task")
    management.call_command("import_welcome_europe", verbosity=1)


@app.task
def task_import_ile_de_france():
    """Import data from the 'Conseil Régional Ile de France' data feed."""
    logger.info("Starting Conseil Régional Ile de France import task")
    management.call_command("import_ile_de_france", verbosity=1)


@app.task
def find_broken_links():
    """Check the reliability of aid associated links"""
    logger.info("Starting find_broken_links task")
    management.call_command("find_broken_links", verbosity=1)


@app.task
def populate_inhabitants_number():
    """Populate the Organization's inhabitants_number field when organization is a commune."""
    logger.info("Starting populate_inhabitants_number task")
    management.call_command("populate_inhabitants_number", verbosity=1)
