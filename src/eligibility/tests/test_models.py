import pytest

from eligibility.models import EligibilityTest
from eligibility.factories import EligibilityTestFactory
from aids.models import Aid
from aids.factories import AidFactory


pytestmark = pytest.mark.django_db


def test_aid_eligibility():
    aid_1 = AidFactory()
    aid_2 = AidFactory()
    eligibility_test_1 = EligibilityTestFactory()
    aid_2.eligibility_test = eligibility_test_1
    aid_2.save()

    assert EligibilityTest.objects.count() == 1
    assert Aid.objects.count() == 2
    assert Aid.objects.has_eligibility_test().count() == 1
    assert aid_1.has_eligibility_test() is False
    assert aid_2.has_eligibility_test() is True
