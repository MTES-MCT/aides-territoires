import requests
from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings

from accounts.models import User


API_HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-key": settings.SIB_API_KEY,
}


class Command(BaseCommand):
    """This script imports data from sendinblue.

    We fetch contact from sendinblue. Then, when fetched contacts correspond
    to known AT accounts, we update said accounts with imported data:

     * the STRUCTURE field is saved to the `organization` User field.
     * when contacts are blacklisted, we untick the `ml_consent` field.
    """

    help = "Import missing data for existing contacts"

    @transaction.atomic
    def handle(self, *args, **options):
        contacts_data = self.fetch_contacts()
        for datum in contacts_data:
            email = datum["email"]
            blacklisted = datum["emailBlacklisted"]
            attrs = datum["attributes"]
            org = attrs.get("STRUCTURE", "")

            self.stdout.write("Update {} {} {}".format(email, org, blacklisted))
            if org:
                User.objects.filter(email=email).update(
                    organization=org, ml_consent=not blacklisted
                )
            else:
                User.objects.filter(email=email).update(ml_consent=not blacklisted)

    def fetch_contacts(self):
        """Fetch *all* contacts using the Brevo API."""
        endpoint = settings.SIB_ENDPOINT

        # First, let's count the number of results
        params = {"limit": "1", "offset": "0"}
        self.stdout.write("Counting data")
        res = requests.get(endpoint, headers=API_HEADERS, params=params)
        data = res.json()
        count = data["count"]

        # Then, send api requests until we got all contacts
        limit = 500
        offset = 0
        contacts_data = []
        while offset < count:
            params = {"limit": limit, "offset": offset}
            self.stdout.write("Fetching data {} to {}".format(offset, offset + limit))
            res = requests.get(endpoint, headers=API_HEADERS, params=params)
            data = res.json()
            contacts_data += data["contacts"]
            offset += limit

        return contacts_data
