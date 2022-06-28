"""Global fixtures for tests."""

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from django.db import connection

from accounts.factories import UserFactory, ContributorFactory
from backers.factories import BackerFactory
from geofr.models import Perimeter
from geofr.factories import PerimeterFactory
from categories.factories import CategoryFactory
from organizations.models import Organization


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute('CREATE TEXT SEARCH CONFIGURATION french_unaccent( COPY = french ); ALTER TEXT SEARCH CONFIGURATION french_unaccent ALTER MAPPING FOR hword, hword_part, word WITH unaccent, french_stem;')  # noqa


@pytest.fixture(scope="module")
def browser():
    opts = Options()
    opts.headless = True
    browser = webdriver.Firefox(options=opts)
    browser.implicitly_wait(1)
    browser.set_window_position(0, 0)
    browser.set_window_size(1200, 800)

    # This is equivalent to a `tearDown`.
    # Sometimes, I admire Python's elegancy so much!
    yield browser
    browser.quit()


@pytest.fixture
def user():
    """Generates a valid and active user."""

    user = UserFactory(email="sample.user@example.org")
    user_org = Organization(name='Sample Org', perimeter=Perimeter.objects.first())
    user_org.save()
    user.beneficiary_organization_id = user_org.pk
    user.organization_type = "farmer"
    user.save()
    return user


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def contributor():
    """Generates a valid and active contributor."""

    # We may need an OrganizationFactory when the organizations app has a test suite
    sample_org = Organization(name="Sample org", organization_type=["commune"])
    sample_org.save()

    user = ContributorFactory()
    user.beneficiary_organization = sample_org
    user.save()
    return user


@pytest.fixture
def superuser():
    """Generates a valid and active superuser."""

    user = UserFactory(email="sample.admin@example.org")
    user.is_superuser = True
    user.save()
    return user


@pytest.fixture
def superuser_client(superuser, client):
    client.force_login(superuser)
    return client


@pytest.fixture
def backer():
    """Generates a valid Backer."""

    backer = BackerFactory()
    return backer


@pytest.fixture
def perimeter():
    """Generates a valid Perimeter."""

    perimeter = PerimeterFactory()
    return perimeter


@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def perimeters():

    europe = PerimeterFactory(
        scale=Perimeter.SCALES.continent,
        name='Europe',
        code='EU')
    france = PerimeterFactory(
        scale=Perimeter.SCALES.country,
        contained_in=[europe],
        name='France',
        code='FRA')
    metropole = PerimeterFactory(
        scale=Perimeter.SCALES.adhoc,
        contained_in=[europe, france],
        name='Métropole',
        code='FRA-MET')
    outre_mer = PerimeterFactory(
        scale=Perimeter.SCALES.adhoc,
        contained_in=[europe, france],
        name='Outre-mer',
        code='FRA-OM')
    rhonemed = PerimeterFactory(
        scale=Perimeter.SCALES.basin,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name='Rhône-Méditerannée',
        country='FRA',
        code='FR000006')
    adour_garonne = PerimeterFactory(
        scale=Perimeter.SCALES.basin,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name='Adour-Garonne',
        code='FR000005')
    occitanie = PerimeterFactory(
        scale=Perimeter.SCALES.region,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name='Occitanie',
        code='76')
    herault = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, occitanie, metropole],
        is_overseas=False,
        name='Hérault',
        code='34',
        regions=['76'])
    montpellier = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, occitanie, herault, rhonemed, metropole],
        is_overseas=False,
        name='Montpellier',
        code='34172',
        regions=['76'],
        departments=['34'],
        basin='FR000006')
    vic = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, occitanie, herault, rhonemed, metropole],
        is_overseas=False,
        name='Vic-la-Gardiole',
        code='34333',
        regions=['76'],
        departments=['34'],
        basin='FR000006')
    aveyron = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, occitanie, metropole],
        is_overseas=False,
        name='Aveyron',
        code='12',
        regions=['76'])
    rodez = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, occitanie, aveyron, adour_garonne,
                      metropole],
        is_overseas=False,
        name='Rodez',
        code='12202',
        regions=['76'],
        departments=['12'],
        basin='FR000005')
    normandie = PerimeterFactory(
        scale=Perimeter.SCALES.region,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name='Normandie',
        code='28')
    eure = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, normandie, metropole],
        is_overseas=False,
        name='Eure',
        code='28',
        regions=['28'])
    st_cyr = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, normandie, eure, metropole],
        is_overseas=False,
        name='Saint-Cyr-la-Campagne',
        code='27529',
        regions=['28'],
        departments=['27'])
    fort_de_france = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
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
