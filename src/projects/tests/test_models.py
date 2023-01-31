import pytest

from projects.factories import ProjectFactory
from projects.models import image_upload_to

pytestmark = pytest.mark.django_db


def test_image_upload_to():
    instance = ProjectFactory(name="Sample project")
    filename = "logo.png"
    upload_path = image_upload_to(instance, filename)

    assert upload_path == f"projects/{instance.slug}_image.png"
