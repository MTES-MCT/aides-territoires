import requests
import json
from django.core.management.base import BaseCommand
from django.conf import settings

from accounts.models import NewsletterUser


API_HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'api-key': settings.SIB_API_KEY,
}


class Command(BaseCommand):
    help = 'Export all newsletterUser to the newsletter provider'

    def handle(self, *args, **options):
        accounts = NewsletterUser.objects.all()[:5]
        for account in accounts:
            self.export_account(account)

    def export_account(self, user):
        endpoint = 'https://api.sendinblue.com/v3/contacts/'
        data = {
            'email': user.email,
            'attributes': {
                'DOUBLE_OPT-IN': 1,
            },
            'emailBlacklisted': not user.ml_consent,
            'listIds': [settings.SIB_LIST_ID],
            'updateEnabled': True,
        }
        requests.post(endpoint, headers=API_HEADERS, data=json.dumps(data))
        self.stdout.write('Exporting {}'.format(user.email))
