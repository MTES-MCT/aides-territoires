import pytest

from geofr.models import Perimeter


pytestmark = pytest.mark.django_db


def test_departments_actually_sorts_departments(perimeters):
    """The Corsican departments are at the '20' position in the list"""
    departments_list = Perimeter.objects.departments(values=["id", "name", "code"])

    dept_19 = [i for i, d in enumerate(departments_list) if "19" in d.values()][0]
    dept_2a = [i for i, d in enumerate(departments_list) if "2A" in d.values()][0]
    dept_2b = [i for i, d in enumerate(departments_list) if "2B" in d.values()][0]
    dept_21 = [i for i, d in enumerate(departments_list) if "21" in d.values()][0]

    assert dept_19 < dept_2a < dept_2b < dept_21


def test_departments_adds_a_slug(perimeters):
    departments_list = Perimeter.objects.departments(values=["id", "name", "code"])

    aveyron = departments_list[0]

    assert aveyron["slug"] == "aveyron"


def test_get_communes_within_radius(perimeters):
    """The method should not return Béziers (too far away)"""
    abeilhan = Perimeter.objects.get(code="34001")
    abeilhan.longitude = 3.3026
    abeilhan.latitude = 43.46
    abeilhan.save()

    beziers = Perimeter.objects.get(code="34032")
    beziers.longitude = 3.2342
    beziers.latitude = 43.3481
    beziers.save()

    montpellier = Perimeter.objects.get(code="34172")
    montpellier.longitude = 3.8742
    montpellier.latitude = 43.61
    montpellier.save()

    vic = Perimeter.objects.get(code="34333")
    vic.longitude = 3.8046
    vic.latitude = 43.4838
    vic.save()

    near_montpellier = montpellier.get_communes_within_radius(50)

    assert abeilhan in near_montpellier
    assert vic in near_montpellier

    assert montpellier in near_montpellier
    assert beziers not in near_montpellier
