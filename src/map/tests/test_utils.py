import pytest
from conftest import perimeter
from geofr.models import Perimeter
from map.utils import get_backers_count_by_department, get_programs_count_by_department

from aids.factories import AidFactory
from backers.factories import BackerFactory

pytestmark = pytest.mark.django_db



def test_get_backers_count_by_department(client, perimeters):
    relevant_dept = Perimeter.objects.get(name="Hérault")
    relevant_city = Perimeter.objects.get(name="Montpellier")
    other_dept = Perimeter.objects.get(name="Eure")
    other_city = Perimeter.objects.get(name="Fort-de-France")

    backer_relevant_dept = BackerFactory(perimeter=relevant_dept)
    backer_relevant_city = BackerFactory(perimeter=relevant_city)
    backer_other_dept = BackerFactory(perimeter=other_dept)
    backer_other_city = BackerFactory(perimeter=other_city)

    relevant_aid_1 = AidFactory(perimeter=relevant_dept)
    backer_relevant_dept.financed_aids.add(relevant_aid_1)
    backer_relevant_dept.save()

    relevant_aid_2 = AidFactory(perimeter=relevant_city)
    relevant_aid_3 = AidFactory(perimeter=relevant_city)
    backer_relevant_city.financed_aids.add(relevant_aid_2)
    backer_relevant_city.financed_aids.add(relevant_aid_3)
    backer_relevant_city.save()

    other_aid_1 = AidFactory(perimeter=other_dept)
    backer_other_dept.financed_aids.add(other_aid_1)
    backer_other_dept.save()

    other_aid_2 = AidFactory(perimeter=other_city)
    backer_other_city.financed_aids.add(other_aid_2)
    backer_other_dept.save()

    backers_count = get_backers_count_by_department(relevant_dept.id).count()
    assert backers_count == 2
