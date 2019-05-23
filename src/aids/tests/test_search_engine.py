"""Test methods for the search engine view."""

import pytest
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone

from aids.factories import AidFactory
from geofr.factories import PerimeterFactory
from geofr.models import Perimeter


pytestmark = pytest.mark.django_db


@pytest.fixture
def perimeters():
    perimeters = {
        'europe': PerimeterFactory(
            scale=Perimeter.TYPES.continent,
            name='Europe',
            code='EU'),
        'france': PerimeterFactory(
            scale=Perimeter.TYPES.country,
            name='France',
            code='FRA'),
        'métropole': PerimeterFactory(
            scale=Perimeter.TYPES.mainland,
            name='Métropole',
            code='FRA-MET'),
        'outre-mer': PerimeterFactory(
            scale=Perimeter.TYPES.overseas,
            name='Outre-mer',
            code='FRA-OM'),
        'occitanie': PerimeterFactory(
            scale=Perimeter.TYPES.region,
            is_overseas=False,
            name='Occitanie',
            code='76'),
        'herault': PerimeterFactory(
            scale=Perimeter.TYPES.department,
            is_overseas=False,
            name='Hérault',
            code='34',
            regions=['76']),
        'montpellier': PerimeterFactory(
            scale=Perimeter.TYPES.commune,
            is_overseas=False,
            name='Montpellier',
            code='34172',
            regions=['76'],
            departments=['34'],
            basin='FR000006'),
        'vic': PerimeterFactory(
            scale=Perimeter.TYPES.commune,
            is_overseas=False,
            name='Vic-la-Gardiole',
            code='34333',
            regions=['76'],
            departments=['34'],
            basin='FR000006'),
        'aveyron': PerimeterFactory(
            scale=Perimeter.TYPES.department,
            is_overseas=False,
            name='Aveyron',
            code='12',
            regions=['76']),
        'rodez': PerimeterFactory(
            scale=Perimeter.TYPES.commune,
            is_overseas=False,
            name='Rodez',
            code='12202',
            regions=['76'],
            departments=['12'],
            basin='FR000005'),
        'normandie': PerimeterFactory(
            scale=Perimeter.TYPES.region,
            is_overseas=False,
            name='Normandie',
            code='28'),
        'eure': PerimeterFactory(
            scale=Perimeter.TYPES.department,
            is_overseas=False,
            name='Eure',
            code='28',
            regions=['28']),
        'st-cyr': PerimeterFactory(
            scale=Perimeter.TYPES.commune,
            is_overseas=False,
            name='Saint-Cyr-la-Campagne',
            code='27529',
            regions=['28'],
            departments=['27']),
        'rhone-mediterannee': PerimeterFactory(
            scale=Perimeter.TYPES.basin,
            is_overseas=False,
            name='Rhône-Méditerannée',
            country='FRA',
            code='FR000006'),
        'adour-garonne': PerimeterFactory(
            scale=Perimeter.TYPES.basin,
            is_overseas=False,
            name='Adour-Garonne',
            code='FR000005'),
        'fort-de-france': PerimeterFactory(
            scale=Perimeter.TYPES.commune,
            is_overseas=True,
            name='Fort-de-France',
            code='97209',
            regions=['02'],
            departments=['972']),
    }
    return perimeters


@pytest.fixture
def aids(perimeters):
    aids = [
        AidFactory(perimeter=perimeters['europe']),
        *AidFactory.create_batch(2, perimeter=perimeters['france']),
        *AidFactory.create_batch(3, perimeter=perimeters['occitanie']),
        *AidFactory.create_batch(4, perimeter=perimeters['herault']),
        *AidFactory.create_batch(5, perimeter=perimeters['montpellier']),
        *AidFactory.create_batch(6, perimeter=perimeters['vic']),
        *AidFactory.create_batch(7, perimeter=perimeters['aveyron']),
        *AidFactory.create_batch(8, perimeter=perimeters['rodez']),
        *AidFactory.create_batch(9, perimeter=perimeters['normandie']),
        *AidFactory.create_batch(10, perimeter=perimeters['eure']),
        *AidFactory.create_batch(11, perimeter=perimeters['st-cyr']),
        *AidFactory.create_batch(12, perimeter=perimeters['adour-garonne']),
        *AidFactory.create_batch(13,
                                 perimeter=perimeters['rhone-mediterannee']),
        *AidFactory.create_batch(14, perimeter=perimeters['fort-de-france']),

    ]
    return aids


def test_seach_engine_view(client):
    """Test that the url is publicly accessible."""

    url = reverse('search_view')
    res = client.get(url)
    assert res.status_code == 200


def test_only_published_aids_are_listed(client):
    """Test that unpublished aids are not shown."""

    AidFactory.create_batch(3)
    url = reverse('search_view')
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 3

    # Let's create some non published aids, to check that the list
    # of objects passed to the context does not change
    AidFactory.create_batch(5, status='draft')
    AidFactory.create_batch(7, status='reviewable')
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 3

    # Let's add some more published aids, to check that the limit does not
    # come from pagination parameters
    AidFactory.create_batch(11)
    url = reverse('search_view')
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 14


def test_deleted_aids_are_not_listed(client):
    """Deleted aids must be excluded from all queries by default."""

    AidFactory(status='deleted')
    url = reverse('search_view')
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 0


def test_expired_aids_are_not_listed(client):

    url = reverse('search_view')

    AidFactory.create_batch(2)
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 2

    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)

    AidFactory.create_batch(3, submission_deadline=tomorrow)
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 5

    AidFactory.create_batch(5, submission_deadline=today)
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 10

    AidFactory.create_batch(7, submission_deadline=yesterday)
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context['aids']) == 10


def test_search_european_aids(client, perimeters, aids):
    """Display ALL the aids."""
    url = reverse('search_view')
    res = client.get(url, data={'perimeter': perimeters['europe'].pk})
    assert res.context['paginator'].count == 105


def test_search_french_aids(client, perimeters, aids):
    """Display ALL the aids again."""
    url = reverse('search_view')
    res = client.get(url, data={'perimeter': perimeters['france'].pk})
    assert res.context['paginator'].count == 105


def test_search_aids_form_occitanie(client, perimeters, aids):
    """Only display aids in Occitanie and above."""
    url = reverse('search_view')
    res = client.get(url, data={'perimeter': perimeters['occitanie'].pk})
    assert res.context['paginator'].count == 36


def test_search_aids_from_herault(client, perimeters, aids):
    """Only display aids in Hérault and above."""
    url = reverse('search_view')
    res = client.get(url, data={'perimeter': perimeters['herault'].pk})
    assert res.context['paginator'].count == 21


def test_search_aids_from_montpellier(client, perimeters, aids):
    """Only display aids in Hérault and above."""
    url = reverse('search_view')
    res = client.get(url, data={'perimeter': perimeters['montpellier'].pk})
    assert res.context['paginator'].count == 28


def test_search_aids_from_rhone_mediterannee_basin(client, perimeters, aids):
    """Only display aids in the selected basin."""

    url = reverse('search_view')
    res = client.get(url, data={
        'perimeter': perimeters['rhone-mediterannee'].pk})
    assert res.context['paginator'].count == 27


def test_search_aids_from_adour_garonne_basin(client, perimeters, aids):
    """Only display aids in the selected basin."""

    url = reverse('search_view')
    res = client.get(url, data={
        'perimeter': perimeters['adour-garonne'].pk})
    assert res.context['paginator'].count == 23


def test_search_mainland_aids(client, perimeters, aids):
    """Only display overseas aids."""

    url = reverse('search_view')
    res = client.get(url, data={'perimeter': perimeters['outre-mer'].pk})
    assert res.context['paginator'].count == 14


def test_search_overseas_aids(client, perimeters, aids):
    """Only display mainland aids."""

    url = reverse('search_view')
    res = client.get(url, data={'perimeter': perimeters['métropole'].pk})
    assert res.context['paginator'].count == 88


def test_full_text_search(client, perimeters):
    """Full text search return valid results."""

    AidFactory(perimeter=perimeters['europe'], name='Mon Aide à Tester')
    url = reverse('search_view')

    # Words are correctly stemmed and lexemed
    res = client.get(url, data={'text': 'aide'})
    assert res.context['paginator'].count == 1

    # Plurals are taken into account
    res = client.get(url, data={'text': 'aides'})
    assert res.context['paginator'].count == 1

    # Verbs are too
    res = client.get(url, data={'text': 'test'})
    assert res.context['paginator'].count == 1

    # Irrelevant results are not returned
    res = client.get(url, data={'text': 'gloubiboulga'})
    assert res.context['paginator'].count == 0


def test_full_text_results_ordering(client, perimeters):
    """Title terms have more weight."""

    europe = perimeters['europe']
    AidFactory(perimeter=europe, name='Pomme', description='Poire')
    AidFactory(perimeter=europe, name='Poire', description='Pomme')
    url = reverse('search_view')

    res = client.get(url, data={'text': 'pomme'})
    assert res.context['paginator'].count == 2
    assert res.context['aids'][0].name == 'Pomme'
    assert res.context['aids'][1].name == 'Poire'

    res = client.get(url, data={'text': 'poire'})
    assert res.context['paginator'].count == 2
    assert res.context['aids'][0].name == 'Poire'
    assert res.context['aids'][1].name == 'Pomme'


def test_full_text_uses_tags(client, perimeters):
    """Users can search in tags."""

    AidFactory(
        perimeter=perimeters['europe'],
        tags=['tartiflette', 'camembert roti', 'gratin dauphinois'])
    url = reverse('search_view')

    res = client.get(url, data={'text': 'gratin'})
    assert res.context['paginator'].count == 1


def test_full_text_advanced_syntax(client, perimeters):
    AidFactory(
        perimeter=perimeters['europe'],
        name='Dépollution des rejets urbains par temps de pluie')
    url = reverse('search_view')

    # Searching with several terms find the document
    res = client.get(url, data={'text': 'dépollution temps pluie'})
    assert res.context['paginator'].count == 1

    # Search terms are ORed
    res = client.get(url, data={'text': 'dépollution temps soleil'})
    assert res.context['paginator'].count == 1

    # Search terms can be excluded
    res = client.get(url, data={'text': 'dépollution temps - pluie'})
    assert res.context['paginator'].count == 0

    res = client.get(url, data={'text': 'dépollution temps - soleil'})
    assert res.context['paginator'].count == 1

    res = client.get(url, data={'text': '- pluie'})
    assert res.context['paginator'].count == 0

    # Search terms can be mandatory
    res = client.get(url, data={'text': 'dépollution temps + soleil'})
    assert res.context['paginator'].count == 0

    # Several terms can be mandatory
    res = client.get(url, data={'text': 'dépollution + temps + pluie'})
    assert res.context['paginator'].count == 1

    # Optional fields are optional
    res = client.get(url, data={'text': 'gratin tartiflette temps + pluie'})
    assert res.context['paginator'].count == 1

    # "+" prefix makes left and right terms mandatory
    res = client.get(url, data={'text': 'gratin tartiflette + temps + pluie'})
    assert res.context['paginator'].count == 0

    # "+" and "-" can be combined
    res = client.get(url, data={
        'text': '- tartiflette + temps + pluie - soleil'})
    assert res.context['paginator'].count == 1


def test_the_call_for_project_only_filter(client, perimeters, aids):

    for aid in aids[:5]:
        aid.is_call_for_project = True
        aid.save()

    url = reverse('search_view')
    res = client.get(url, data={'call_for_projects_only': 'Oui'})
    assert res.context['paginator'].count == 5


def test_submission_deadline_ordering(client, perimeters):
    """Test that results can be sorted by approaching deadline."""

    AidFactory(
        name='Approaching aid',
        perimeter=perimeters['europe'],
        submission_deadline=timezone.now() + timedelta(days=5))
    AidFactory(
        name='Plenty of time aid',
        perimeter=perimeters['france'],
        submission_deadline=timezone.now() + timedelta(days=150))

    url = reverse('search_view')

    res = client.get(url)
    assert res.context['paginator'].count == 2
    assert res.context['aids'][0].name == 'Plenty of time aid'
    assert res.context['aids'][1].name == 'Approaching aid'

    res = client.get(url, data={'order_by': 'submission_deadline'})
    assert res.context['paginator'].count == 2
    assert res.context['aids'][0].name == 'Approaching aid'
    assert res.context['aids'][1].name == 'Plenty of time aid'
