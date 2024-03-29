"""Global fixtures for tests."""

import environ
from os import path
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from accounts.factories import UserFactory, ContributorFactory
from aids.factories import AidFactory
from aids.resources import ADMIN_EMAIL
from backers.factories import BackerFactory
from geofr.models import Perimeter
from geofr.factories import PerimeterFactory
from categories.factories import CategoryFactory
from organizations.factories import OrganizationFactory

# Conftest does not seem to load the Django settings
environ.Env.read_env(".env.local")
env = environ.Env()


@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument("-headless")

    geckodriver_path = env("GECKODRIVER_PATH", default="")
    if geckodriver_path:
        service = Service(executable_path=geckodriver_path, log_path=path.devnull)
        browser = webdriver.Firefox(options=options, service=service)
    else:
        browser = webdriver.Firefox(options=options)
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

    user = UserFactory()
    user_org = OrganizationFactory(perimeter=Perimeter.objects.first())
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

    sample_org = OrganizationFactory(
        organization_type=["commune"],
        perimeter=Perimeter.objects.first(),
    )
    sample_org.save()

    user = ContributorFactory()
    user.beneficiary_organization = sample_org
    user.save()

    sample_org.beneficiaries.add(user)
    return user


@pytest.fixture
def superuser():
    """Generates a valid and active superuser."""
    sample_org = OrganizationFactory(
        organization_type=["private_person"],
        perimeter=Perimeter.objects.first(),
    )
    sample_org.save()

    user = UserFactory(email=ADMIN_EMAIL, first_name="Super", last_name="User")
    user.is_superuser = True
    user.beneficiary_organization = sample_org
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
        scale=Perimeter.SCALES.continent, name="Europe", code="EU"
    )
    france = PerimeterFactory(
        scale=Perimeter.SCALES.country, contained_in=[europe], name="France", code="FRA"
    )
    metropole = PerimeterFactory(
        scale=Perimeter.SCALES.adhoc,
        contained_in=[europe, france],
        name="Métropole",
        code="FRA-MET",
    )
    outre_mer = PerimeterFactory(
        scale=Perimeter.SCALES.adhoc,
        contained_in=[europe, france],
        name="Outre-mer",
        code="FRA-OM",
    )
    rhonemed = PerimeterFactory(
        scale=Perimeter.SCALES.basin,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name="Rhône-Méditerannée",
        country="FRA",
        code="FR000006",
    )
    adour_garonne = PerimeterFactory(
        scale=Perimeter.SCALES.basin,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name="Adour-Garonne",
        code="FR000005",
    )
    occitanie = PerimeterFactory(
        scale=Perimeter.SCALES.region,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name="Occitanie",
        code="76",
    )
    herault = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, occitanie, metropole],
        is_overseas=False,
        name="Hérault",
        code="34",
        regions=["76"],
    )
    montpellier = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, occitanie, herault, rhonemed, metropole],
        is_overseas=False,
        name="Montpellier",
        code="34172",
        regions=["76"],
        departments=["34"],
        basin="FR000006",
    )
    vic = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, occitanie, herault, rhonemed, metropole],
        is_overseas=False,
        name="Vic-la-Gardiole",
        code="34333",
        regions=["76"],
        departments=["34"],
        basin="FR000006",
    )
    abeilhan = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, occitanie, herault, rhonemed, metropole],
        is_overseas=False,
        name="Abeilhan",
        code="34001",
        regions=["76"],
        departments=["34"],
        basin="FR000006",
    )
    beziers = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, occitanie, herault, rhonemed, metropole],
        is_overseas=False,
        name="Béziers",
        code="34032",
        regions=["76"],
        departments=["34"],
        basin="FR000006",
    )
    aveyron = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, occitanie, metropole],
        is_overseas=False,
        name="Aveyron",
        code="12",
        regions=["76"],
    )
    rodez = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, occitanie, aveyron, adour_garonne, metropole],
        is_overseas=False,
        name="Rodez",
        code="12202",
        regions=["76"],
        departments=["12"],
        basin="FR000005",
    )
    normandie = PerimeterFactory(
        scale=Perimeter.SCALES.region,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name="Normandie",
        code="28",
    )
    eure = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, normandie, metropole],
        is_overseas=False,
        name="Eure",
        code="28",
        regions=["28"],
    )
    st_cyr = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, normandie, eure, metropole],
        is_overseas=False,
        name="Saint-Cyr-la-Campagne",
        code="27529",
        regions=["28"],
        departments=["27"],
    )
    fort_de_france = PerimeterFactory(
        scale=Perimeter.SCALES.commune,
        contained_in=[europe, france, outre_mer],
        is_overseas=True,
        name="Fort-de-France",
        code="97209",
        regions=["02"],
        departments=["972"],
    )
    nouvelle_aquitaine = PerimeterFactory(
        scale=Perimeter.SCALES.region,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name="Nouvelle-Aquitaine",
        code="75",
    )
    correze = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, nouvelle_aquitaine, metropole],
        is_overseas=False,
        name="Corrèze",
        code="19",
        regions=["75"],
    )
    corse = PerimeterFactory(
        scale=Perimeter.SCALES.region,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name="Corse",
        code="94",
    )
    corse_du_sud = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, corse, metropole],
        is_overseas=False,
        name="Corse-du-Sud",
        code="2A",
        regions=["94"],
    )
    haute_corse = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, corse, metropole],
        is_overseas=False,
        name="Haute-Corse",
        code="2B",
        regions=["94"],
    )
    bourgogne = PerimeterFactory(
        scale=Perimeter.SCALES.region,
        contained_in=[europe, france, metropole],
        is_overseas=False,
        name="Bourgogne",
        code="26",
    )
    cote_dor = PerimeterFactory(
        scale=Perimeter.SCALES.department,
        contained_in=[europe, france, bourgogne, metropole],
        is_overseas=False,
        name="Côte-d’Or",
        code="21",
        regions=["26"],
    )

    perimeters = {
        "europe": europe,
        "france": france,
        "métropole": metropole,
        "outre-mer": outre_mer,
        "occitanie": occitanie,
        "herault": herault,
        "montpellier": montpellier,
        "vic": vic,
        "abeilhan": abeilhan,
        "beziers": beziers,
        "aveyron": aveyron,
        "rodez": rodez,
        "normandie": normandie,
        "eure": eure,
        "st-cyr": st_cyr,
        "rhone-mediterannee": rhonemed,
        "adour-garonne": adour_garonne,
        "fort-de-france": fort_de_france,
        "nouvelle-aquitaine": nouvelle_aquitaine,
        "correze": correze,
        "corse": corse,
        "corse-du-sud": corse_du_sud,
        "haute-corse": haute_corse,
        "bourgogne": bourgogne,
        "cote-dor": cote_dor,
    }
    return perimeters


@pytest.fixture
def aids(perimeters):
    aids = [
        AidFactory(perimeter=perimeters["europe"]),
        *AidFactory.create_batch(2, perimeter=perimeters["france"]),
        *AidFactory.create_batch(3, perimeter=perimeters["occitanie"]),
        *AidFactory.create_batch(4, perimeter=perimeters["herault"]),
        *AidFactory.create_batch(5, perimeter=perimeters["montpellier"]),
        *AidFactory.create_batch(6, perimeter=perimeters["vic"]),
        *AidFactory.create_batch(7, perimeter=perimeters["aveyron"]),
        *AidFactory.create_batch(8, perimeter=perimeters["rodez"]),
        *AidFactory.create_batch(9, perimeter=perimeters["normandie"]),
        *AidFactory.create_batch(10, perimeter=perimeters["eure"]),
        *AidFactory.create_batch(11, perimeter=perimeters["st-cyr"]),
        *AidFactory.create_batch(12, perimeter=perimeters["adour-garonne"]),
        *AidFactory.create_batch(13, perimeter=perimeters["rhone-mediterannee"]),
        *AidFactory.create_batch(14, perimeter=perimeters["fort-de-france"]),
        *AidFactory.create_batch(15, perimeter=perimeters["outre-mer"]),
    ]
    return aids
