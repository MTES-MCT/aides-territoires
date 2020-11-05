import os

import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from upload.models import UploadImage


pytestmark = pytest.mark.django_db

IMAGE_PATH = os.path.join(os.getcwd(), "upload/tests/data/test-image.png")

User = get_user_model()


def upload_image(client):
    url = reverse('upload_image')
    with open(IMAGE_PATH, 'rb') as img:
        post_data = {'alt': 'test image', 'image': img}
        response = client.post(url, post_data, format='multipart')
    return response


def test_superuser_can_post_to_upload_view(client, superuser):
    client.force_login(superuser)
    response = upload_image(client)
    assert response.status_code == 200


def test_annonymous_cannot_post_to_upload_view(client):
    client.logout()
    response = upload_image(client)
    assert response.status_code == 302


def test_superuser_can_upload_an_image(client, superuser):
    client.force_login(superuser)
    count_before = UploadImage.objects.count()
    upload_image(client)
    count_after = UploadImage.objects.count()
    assert count_after == count_before + 1


def test_annonymous_cannot_upload_an_image(client):
    client.logout()
    count_before = UploadImage.objects.count()
    upload_image(client)
    count_after = UploadImage.objects.count()
    assert count_after == count_before


def test_upload_with_empty_data_fail_gracefully(client, superuser):
    client.force_login(superuser)
    url = reverse('upload_image')
    empty_data = {}
    response = client.post(url, empty_data)
    assert response.status_code == 200
    assert '"success": false' in response.content.decode()
