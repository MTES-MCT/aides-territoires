import pytest

from dataproviders.utils import content_prettify, get_category_list_from_name
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
