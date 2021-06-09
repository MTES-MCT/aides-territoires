from django.utils.translation import gettext_lazy as _


COLLECTIVITIES_AUDIENCES = (
    ('commune', _('Communes')),
    ('epci', _('Audience EPCI')),
    ('department', _('Departments')),
    ('region', _('Regions')),
    ('special', _('Special status for outre-mer')),
)

OTHER_AUDIENCES = (
    ('association', _('Associations')),
    ('private_person', _('Individuals')),
    ('farmer', _('Farmers')),
    ('private_sector', _('Private sector')),
    ('public_cies', _('Local public companies')),
    ('public_org', _('Public organizations / State services')),
    ('researcher', _('Research')),
)

AUDIENCES_GROUPED = (
    (_('Collectivities'), COLLECTIVITIES_AUDIENCES),
    (_('Other audiences'), OTHER_AUDIENCES)
)
