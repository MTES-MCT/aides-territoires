from core.templatetags.settings import phone, cloud_file_url


def test_phone_number_is_converted():
    assert phone("+33123456789") == "01 23 45 67 89"
    assert phone("0123456789") == "01 23 45 67 89"


def test_cloud_file_url():
    assert (
        cloud_file_url("test_file.mp4")
        == "https://cloud.example.org/test-bucket/upload/test_file.mp4"
    )
