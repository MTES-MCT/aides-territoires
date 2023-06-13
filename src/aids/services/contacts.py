import logging
import re

from aids.models import Aid

logger = logging.getLogger("console_log")


def extract_aids_contact_info():
    """
    For each aid, try to extract the contact phone and email if
    they are not already there.

    If there are several phones or emails, only the first is used
    """
    aids = Aid.objects.filter(contact__isnull=False)

    logger.debug(f"{aids.count()} aids found.")
    updated_count = 0

    for aid in aids:
        logger.debug(f"Parsing contacts for aid {aid.id} – {aid.name}")
        updated = False

        if not aid.contact_phone:
            phone_regex = r"(0\d[\s-]?\d\d[\s-]?\d\d[\s-]?\d\d[\s-]?\d\d)"
            phone_numbers = re.findall(phone_regex, aid.contact)
            if len(phone_numbers):
                aid.contact_phone = phone_numbers[0]
                updated = True

        if not aid.contact_email:
            email_regex = r"[A-Za-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
            email_addresses = re.findall(email_regex, aid.contact)
            if len(email_addresses):
                aid.contact_email = email_addresses[0]
                updated = True

        if updated:
            aid.contact_info_updated = True
            aid.save()
            updated_count += 1

    logger.info(f"{updated_count} aids updated")
