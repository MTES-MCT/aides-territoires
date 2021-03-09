import requests
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import User


API_HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'api-key': settings.SIB_API_KEY,
}


class Command(BaseCommand):
    help = 'Export all accounts to the newsletter provider'

    def handle(self, *args, **options):
        accounts = User.objects.filter(email__in=['TODO'])
        for account in accounts:
            self.export_account(account)

    def export_account(self, user):
        endpoint = 'https://api.sendinblue.com/v3/contacts/'
        existing_aids = user.aid_set.existing()
        live_aids = existing_aids.live().order_by('date_published')
        latest_published = live_aids.last()
        draft_aids = existing_aids.drafts().order_by('date_created')
        latest_draft = draft_aids.last()
        attributes = {
            'PRENOM': user.first_name,
            'NOM': user.last_name,
            'NOMBRE_AIDES_ACTIVES': existing_aids.count(),
            'DATE_CREATION_COMPTE': user.date_joined.isoformat(),
            'NOMBRE_AIDES_BROUILLONS': draft_aids.count(),
            'NOMBRE_AIDES_AFICHEES': live_aids.count()
        }
        if latest_draft:
            draft_date = latest_draft.date_created.isoformat()
            attributes.update({
                'DATE_DERNIER_BROUILLON': draft_date
            })
        if latest_published:
            published_date = latest_published.date_published.isoformat()
            attributes.update({
                'DATE_DERNIERE_AIDE_PUBLIEE': published_date,
            })
        data = {
            'email': user.email,
            'attributes': attributes,
            'listIds': [settings.SIB_EXPORT_CONTACTS_LIST_ID],
            'updateEnabled': True,
        }
        requests.post(endpoint, headers=API_HEADERS, data=json.dumps(data))
        self.stdout.write('Exporting {}'.format(user.email))
        self.stdout.write('Exporting {}'.format(data))
