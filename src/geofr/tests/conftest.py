import pytest
from geofr.factories import PerimeterFactory
from geofr.models import Perimeter


@pytest.fixture
def perimeters():

    europe = PerimeterFactory(
        scale=Perimeter.TYPES.continent,
        name='Europe',
        code='EU')
    france = PerimeterFactory(
        scale=Perimeter.TYPES.country,
        contained_in=[europe],
        name='France',
        code='FRA')
    metropole = PerimeterFactory(
        scale=Perimeter.TYPES.adhoc,
        contained_in=[europe, france],
        name='Métropole',
        code='FRA-MET')
    outre_mer = PerimeterFactory(
        scale=Perimeter.TYPES.adhoc,
        contained_in=[europe, france],
        name='Outre-mer',
        code='FRA-OM')
    rhonemed = PerimeterFactory(
        scale=Perimeter.TYPES.basin,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name='Rhône-Méditerannée',
        country='FRA',
        code='FR000006')
    adour_garonne = PerimeterFactory(
        scale=Perimeter.TYPES.basin,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name='Adour-Garonne',
        code='FR000005')
    occitanie = PerimeterFactory(
        scale=Perimeter.TYPES.region,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name='Occitanie',
        code='76')
    herault = PerimeterFactory(
        scale=Perimeter.TYPES.department,
        contained_in=[europe, france, occitanie, metropole],
        is_overseas=False,
        name='Hérault',
        code='34',
        regions=['76'])
    montpellier = PerimeterFactory(
        scale=Perimeter.TYPES.commune,
        contained_in=[europe, france, occitanie, herault, rhonemed, metropole],
        is_overseas=False,
        name='Montpellier',
        code='34172',
        regions=['76'],
        departments=['34'],
        basin='FR000006')
    vic = PerimeterFactory(
        scale=Perimeter.TYPES.commune,
        contained_in=[europe, france, occitanie, herault, rhonemed, metropole],
        is_overseas=False,
        name='Vic-la-Gardiole',
        code='34333',
        regions=['76'],
        departments=['34'],
        basin='FR000006')
    aveyron = PerimeterFactory(
        scale=Perimeter.TYPES.department,
        contained_in=[europe, france, occitanie, metropole],
        is_overseas=False,
        name='Aveyron',
        code='12',
        regions=['76'])
    rodez = PerimeterFactory(
        scale=Perimeter.TYPES.commune,
        contained_in=[europe, france, occitanie, aveyron, adour_garonne,
                      metropole],
        is_overseas=False,
        name='Rodez',
        code='12202',
        regions=['76'],
        departments=['12'],
        basin='FR000005')
    normandie = PerimeterFactory(
        scale=Perimeter.TYPES.region,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name='Normandie',
        code='28')
    eure = PerimeterFactory(
        scale=Perimeter.TYPES.department,
        contained_in=[europe, france, normandie, metropole],
        is_overseas=False,
        name='Eure',
        code='28',
        regions=['28'])
    st_cyr = PerimeterFactory(
        scale=Perimeter.TYPES.commune,
        contained_in=[europe, france, normandie, eure, metropole],
        is_overseas=False,
        name='Saint-Cyr-la-Campagne',
        code='27529',
        regions=['28'],
        departments=['27'])
    fort_de_france = PerimeterFactory(
        scale=Perimeter.TYPES.commune,
        contained_in=[europe, france, outre_mer],
        is_overseas=True,
        name='Fort-de-France',
        code='97209',
        regions=['02'],
        departments=['972'])

    perimeters = {
        'europe': europe,
        'france': france,
        'métropole': metropole,
        'outre-mer': outre_mer,
        'occitanie': occitanie,
        'herault': herault,
        'montpellier': montpellier,
        'vic': vic,
        'aveyron': aveyron,
        'rodez': rodez,
        'normandie': normandie,
        'eure': eure,
        'st-cyr': st_cyr,
        'rhone-mediterannee': rhonemed,
        'adour-garonne': adour_garonne,
        'fort-de-france': fort_de_france,
    }
    return perimeters
