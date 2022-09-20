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
