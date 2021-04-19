import pytest

from geofr.utils import (department_from_zipcode, is_overseas,
                         get_all_related_perimeter_ids,
                         attach_perimeters, attach_epci_perimeters)
from geofr.factories import Perimeter, PerimeterFactory


pytestmark = pytest.mark.django_db


def test_department_from_zipcode():
    assert department_from_zipcode('34110') == '34'
    assert department_from_zipcode('27370') == '27'
    assert department_from_zipcode('97200') == '972'
    assert department_from_zipcode('97414') == '974'


def test_is_overseas():
    assert not is_overseas('34110')
    assert not is_overseas('27370')
    assert is_overseas('97200')
    assert is_overseas('97414')


def test_get_all_related_perimeter_ids(perimeters):
    """Finding related perimeters works as expected."""

    related_perimeters_france = get_all_related_perimeter_ids(perimeters['herault'].id)  # noqa

    assert {'id': perimeters['france'].id} in related_perimeters_france
    assert {'id': perimeters['montpellier'].id} in related_perimeters_france
    assert {'id': perimeters['aveyron'].id} not in related_perimeters_france


def test_attach_perimeters(perimeters):
    """Attaching perimeters works as expected."""

    adhoc = PerimeterFactory(
        name='Communes littorales',
        scale=Perimeter.TYPES.adhoc)
    attach_perimeters(
        adhoc,
        ['34333', '97209'])  # Vic-la-gardiole, Fort-de-France

    assert adhoc in perimeters['vic'].contained_in.all()
    assert adhoc in perimeters['herault'].contained_in.all()
    assert adhoc in perimeters['occitanie'].contained_in.all()
    assert adhoc in perimeters['métropole'].contained_in.all()
    assert adhoc in perimeters['outre-mer'].contained_in.all()

    # Make sure perimeter does not contain itself
    assert adhoc not in adhoc.contained_in.all()

    # Make sure france and europe are not contained in the adhoc perimeter
    assert adhoc not in perimeters['france'].contained_in.all()
    assert adhoc not in perimeters['europe'].contained_in.all()


def test_attach_perimeters_cleans_old_data(perimeters):
    """Attaching perimeters removes all other attachments."""

    adhoc = PerimeterFactory(
        name='Communes littorales',
        scale=Perimeter.TYPES.adhoc)
    perimeters['rodez'].contained_in.add(adhoc)
    attach_perimeters(
        adhoc,
        ['34333', '97209'])  # Vic-la-gardiole, Fort-de-France

    assert adhoc not in perimeters['rodez'].contained_in.all()


def test_attach_epci_perimeters(perimeters):
    """Attaching epci perimeters works as expected."""

    epci_1 = PerimeterFactory(
        name='EPCI 1',
        scale=Perimeter.TYPES.epci)
    perimeters['vic'].contained_in.add(epci_1)
    perimeters['herault'].contained_in.add(epci_1)

    epci_2 = PerimeterFactory(
        name='EPCI 2',
        scale=Perimeter.TYPES.epci)
    perimeters['rodez'].contained_in.add(epci_2)

    adhoc = PerimeterFactory(
        name='Syndicat mixte',
        scale=Perimeter.TYPES.adhoc)

    attach_epci_perimeters(
        adhoc,
        [epci_1.name, epci_2.name])

    assert adhoc in perimeters['vic'].contained_in.all()
    assert adhoc in perimeters['herault'].contained_in.all()
    assert adhoc in perimeters['vic'].contained_in.all()
