import re
from html import unescape
from unicodedata import normalize
from bs4 import BeautifulSoup as bs


def content_prettify(raw_text):
    """Clean imported data.

    We import data from many data sources, and it's not always directly
    usable to say the least. This method performs a list of several
    content beautification so we can safely include ugly data on our site:

     * removes escaped html characters
     * removes manual styles from html tags
     * converts weird quote chars and use standard chars instead
     * normalize unicode characters
     * autoindent existing html

    """
    unescaped = unescape(raw_text or '')
    unstyled = re.sub(' style="[^"]+"', '', unescaped)
    unquoted = unstyled \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace('’', "'")
    normalized = normalize('NFKC', unquoted)
    soup = bs(normalized, features='html.parser')
    prettified = soup.prettify()
    return prettified
