from core.templatetags.settings import phone


def test_phone_number_is_converted():
    assert phone("+33123456789") == "01 23 45 67 89"
    assert phone("0123456789") == "01 23 45 67 89"
