import pytest
from geofr.utils import department_from_zipcode, is_overseas, attach_perimeters
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


def test_attach_perimeters(perimeters):
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
    assert adhoc not in perimeters['france'].contained_in.all()
    assert adhoc not in perimeters['europe'].contained_in.all()


def test_attach_perimeters_cleans_old_data(perimeters):
    adhoc = PerimeterFactory(
        name='Communes littorales',
        scale=Perimeter.TYPES.adhoc)
    perimeters['rodez'].contained_in.add(adhoc)
    attach_perimeters(
        adhoc,
        ['34333', '97209'])  # Vic-la-gardiole, Fort-de-France

    assert adhoc not in perimeters['rodez'].contained_in.all()
