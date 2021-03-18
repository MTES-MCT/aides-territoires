from model_utils import Choices

from django.utils.translation import gettext_lazy as _


IMPORT_LICENCES = Choices(
    ('unknown', _('Unknown')),
    ('openlicence20', _('Open licence 2.0')),
)

FREQUENCIES = Choices(
    ('once', _('Once')),
    ('daily', _('Daily')),
    ('weekly', _('Weekly')),
    ('monthly', _('Monthly')),
    ('yearly', _('Yearly'))
)
