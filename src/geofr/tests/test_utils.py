from geofr.utils import department_from_zipcode, is_overseas


def test_department_from_zipcode():
    assert department_from_zipcode('34110') == '34'
    assert department_from_zipcode('27370') == '27'
    assert department_from_zipcode('97200') == '972'
    assert department_from_zipcode('97414') == '974'


def test_is_overseas():
    assert not is_overseas('34110')
    assert not is_overseas('27370')
    assert is_overseas('97200')
    assert is_overseas('97414')
