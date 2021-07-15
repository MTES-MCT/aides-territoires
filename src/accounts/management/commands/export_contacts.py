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
        allowed = settings.ENV_NAME == 'production' and settings.EXPORT_CONTACTS_ENABLED  # noqa
        if not allowed:
            self.stdout.write('Command not allowed on this environment')
            return
        accounts = User.objects.filter(last_login__isnull=False)
        for account in accounts:
            self.export_account(account)

    def export_account(self, user):
        endpoint = 'https://api.sendinblue.com/v3/contacts/'
        existing_aids = user.aids.existing()
        live_aids = existing_aids.live().order_by('date_published')
        latest_published = live_aids.last()
        draft_aids = existing_aids.drafts().order_by('date_created')
        latest_draft = draft_aids.last()
        expired_aids = existing_aids.expired().order_by('submission_deadline')
        latest_expired = expired_aids.last()

        attributes = {
            'PRENOM': user.first_name,
            'NOM': user.last_name,
            'NOMBRE_AIDES_ACTIVES': existing_aids.count(),
            'DATE_CREATION_COMPTE': user.date_created.isoformat(),
            'NOMBRE_AIDES_BROUILLONS': draft_aids.count(),
            'NOMBRE_AIDES_AFICHEES': live_aids.count(),
            'NOMBRE_AIDES_EXPIREES': expired_aids.count(),
            'DATE_DERNIERE_AIDE_PUBLIEE': None,
            'DATE_DERNIER_BROUILLON': None,
            'DATE_DERNIERE_EXPIRATION': None,
        }
        if latest_published:
            published_date = latest_published.date_published.isoformat()
            attributes.update({
                'DATE_DERNIERE_AIDE_PUBLIEE': published_date,
            })
        if latest_draft:
            draft_date = latest_draft.date_created.isoformat()
            attributes.update({
                'DATE_DERNIER_BROUILLON': draft_date
            })
        if latest_expired:
            expiration_date = latest_expired.submission_deadline.isoformat()
            attributes.update({
                'DATE_DERNIERE_EXPIRATION': expiration_date
            })
        data = {
            'email': user.email,
            'attributes': attributes,
            'listIds': [settings.SIB_EXPORT_CONTACTS_LIST_ID],
            'updateEnabled': True,
        }
        requests.post(endpoint, headers=API_HEADERS, data=json.dumps(data))
        self.stdout.write('Exporting {}'.format(user.email))
