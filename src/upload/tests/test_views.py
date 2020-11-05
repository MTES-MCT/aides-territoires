import pytest
from django.urls import reverse

from upload.models import UploadImage

pytestmark = pytest.mark.django_db


def test_upload_view_accept_post(client):
    url = reverse('upload_image')
    res = client.post(url)
    assert res.status_code == 200


def test_upload_view_creates_an_image(client):
    url = reverse('upload_image')
    count_before = UploadImage.objects.count()
    res = client.post(url)
    count_after = UploadImage.objects.count()
    assert res.status_code == 200
    assert count_after == count_before + 1


# def test_annonymous_cannot_upload_image(client):
#     url = reverse('upload_image')
#     res = client.post(url)
#     assert res.status_code == 200
