import pytest

from dataproviders.utils import (
    content_prettify,
    get_category_list_from_name, extract_mapping_values_from_list)
from aids.models import Aid
from categories.factories import ThemeFactory, CategoryFactory


pytestmark = pytest.mark.django_db


def test_prettify_creates_absolute_urls():

    # Relative urls are made absolute
    html = '''
    This is a <a href="/toto.html">long text with a link</a>
    '''
    text = content_prettify(html, base_url='https://www.example.org')
    assert '<a href="https://www.example.org/toto.html">' in text

    # Absolute urls are left untouched
    html = '''
    This is a <a href="https://www.example.org/toto.html">long text
    with a link</a>
    '''
    text = content_prettify(html, base_url='https://www.example.org')
    assert '<a href="https://www.example.org/toto.html">' in text

    # Urls for other domains are left untouched
    html = '''
    This is a <a href="https://www.example.com/toto.html">long text
    with a link</a>
    '''
    text = content_prettify(html, base_url='https://www.example.org')
    assert '<a href="https://www.example.com/toto.html">' in text


def test_get_category_list_from_name():
    category_1 = CategoryFactory(name='Category 1')
    category_2 = CategoryFactory(name='Category 2')
    theme = ThemeFactory(name='Theme 1')
    theme.categories.set([category_1, category_2])

    category_list = get_category_list_from_name('Category 1')
    assert len(category_list) == 1

    category_list = get_category_list_from_name('Theme 1')
    assert len(category_list) == 2


def test_extract_mapping_values_from_list_of_dicts(capfd):
    mapping_dict = {
        'Asso': [Aid.AUDIENCES.association],
        'Jeunes': [Aid.AUDIENCES.private_person],
        'Autres': [Aid.AUDIENCES.farmer, Aid.AUDIENCES.private_sector]
    }

    list_of_elems_1 = [
        {'name': 'Asso'},
        {'name': 'Jeunes'}
    ]
    output = [Aid.AUDIENCES.association, Aid.AUDIENCES.private_person]
    result = extract_mapping_values_from_list(mapping_dict, list_of_elems=list_of_elems_1, dict_key='name')  # noqa
    assert output == result

    list_of_elems_2 = [
        {'name': 'Asso'},
        {'name': 'Autres'}
    ]
    output = [Aid.AUDIENCES.association, Aid.AUDIENCES.farmer, Aid.AUDIENCES.private_sector]
    result = extract_mapping_values_from_list(mapping_dict, list_of_elems=list_of_elems_2, dict_key='name')  # noqa
    assert output == result

    list_of_elems_3 = [
        {'name': 'Autre'}
    ]
    output = []
    result = extract_mapping_values_from_list(mapping_dict, list_of_elems=list_of_elems_3, dict_key='name')  # noqa
    out, err = capfd.readouterr()
    assert output == result
    assert len(out)


def test_extract_mapping_values_from_list_of_strings(capfd):
    mapping_dict = {
        'Asso': [Aid.AUDIENCES.association],
        'Jeunes': [Aid.AUDIENCES.private_person],
        'Autres': [Aid.AUDIENCES.farmer, Aid.AUDIENCES.private_sector]
    }

    list_of_elems_1 = ['Asso', 'Jeunes']
    output = [Aid.AUDIENCES.association, Aid.AUDIENCES.private_person]
    result = extract_mapping_values_from_list(mapping_dict, list_of_elems=list_of_elems_1)
    assert output == result

    list_of_elems_2 = ['Asso', 'Autres']
    output = [Aid.AUDIENCES.association, Aid.AUDIENCES.farmer, Aid.AUDIENCES.private_sector]
    result = extract_mapping_values_from_list(mapping_dict, list_of_elems=list_of_elems_2)
    assert output == result

    list_of_elems_3 = ['Autre']
    output = []
    result = extract_mapping_values_from_list(mapping_dict, list_of_elems=list_of_elems_3)
    out, err = capfd.readouterr()
    assert output == result
    assert len(out)
