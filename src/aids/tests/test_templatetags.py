import pytest

from aids.factories import AidFactory
from aids.templatetags.aids import financers_type_display
from backers.factories import BackerFactory

pytestmark = pytest.mark.django_db


def test_financers_type_display():
    corporate_backer = BackerFactory(is_corporate=True)
    aid_1 = AidFactory(
        financers=[corporate_backer],
    )
    assert financers_type_display(aid_1) == "PORTEUR D'AIDE PRIVÉ"

    public_backer = BackerFactory(is_corporate=False)
    aid_2 = AidFactory(
        financers=[public_backer],
    )
    assert financers_type_display(aid_2) == "PORTEUR D'AIDE PUBLIC"

    aid_3 = AidFactory(
        financers=[public_backer, corporate_backer],
    )

    assert financers_type_display(aid_3) == "PORTEURS D'AIDE PUBLIC ET PRIVÉ"
