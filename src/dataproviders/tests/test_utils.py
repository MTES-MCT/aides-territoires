from dataproviders.utils import content_prettify


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
