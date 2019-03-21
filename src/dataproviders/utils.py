from html import unescape
from unicodedata import normalize
from bs4 import BeautifulSoup as bs

REMOVABLE_TAGS = ['script', 'style']
ALLOWED_TAGS = [
    'p', 'ul', 'ol', 'li', 'strong', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
]


def content_prettify(raw_text):
    """Clean imported data.

    We import data from many data sources, and it's not always directly
    usable to say the least. This method performs a list of several
    content beautification so we can safely include ugly data on our site:

     * removes escaped html characters
     * converts weird quote chars and use standard chars instead
     * normalize unicode characters
     * removes all `script` html tags
     * removes most of html tags (but leave their content)
     * removes all html tag attributes
     * autoindent existing html

    """
    unescaped = unescape(raw_text or '')
    unquoted = unescaped \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace('’', "'")
    normalized = normalize('NFKC', unquoted)
    soup = bs(normalized, features='html.parser')
    tags = soup.find_all()
    for tag in tags:
        if tag.name in REMOVABLE_TAGS:
            tag.decompose()
        else:
            if tag.name in ALLOWED_TAGS:
                tag.attrs = {}
            else:
                tag.unwrap()
    prettified = soup.prettify()
    return prettified
