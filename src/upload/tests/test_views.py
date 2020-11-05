import os

import pytest
from django.urls import reverse

from upload.models import UploadImage

pytestmark = pytest.mark.django_db


IMAGE_PATH = os.path.join(os.getcwd(), "upload/tests/data/test-image.png")


def test_upload_view_accept_post(client):
    url = reverse('upload_image')
    with open(IMAGE_PATH, 'rb') as img:
        post_data = {'alt': 'test image', 'image': img}
        response = client.post(url, post_data, format='multipart')
    assert response.status_code == 200


def test_upload_view_creates_an_image(client):
    url = reverse('upload_image')
    count_before = UploadImage.objects.count()
    with open(IMAGE_PATH, 'rb') as img:
        post_data = {'alt': 'test image', 'image': img}
        response = client.post(url, post_data, format='multipart')
    count_after = UploadImage.objects.count()
    assert response.status_code == 200
    assert count_after == count_before + 1


def test_upload_with_empty_data_return_false(client):
    url = reverse('upload_image')
    empty_data = {}
    response = client.post(url, empty_data)
    assert response.status_code == 200
    assert '"success": false' in response.content.decode()


# def test_annonymous_cannot_upload_image(client):
#     url = reverse('upload_image')
#     res = client.post(url)
#     assert res.status_code == 200
