import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_perimeter_upload(admin_client, perimeters):
    pass