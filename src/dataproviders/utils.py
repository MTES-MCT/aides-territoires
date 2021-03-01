from html import unescape
from unicodedata import normalize
from bs4 import BeautifulSoup as bs

REMOVABLE_TAGS = ['script', 'style']
ALLOWED_TAGS = [
    'p', 'ul', 'ol', 'li', 'strong', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'br',
]
ALLOWED_ATTRS = ['href', 'src', 'alt', 'width', 'height', 'style', 'target',
                 'rel']


def content_prettify(raw_text, more_allowed_tags=[], more_allowed_attrs=[]):
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
    allowed_tags = ALLOWED_TAGS + more_allowed_tags
    allowed_attrs = ALLOWED_ATTRS + more_allowed_attrs

    unescaped = unescape(raw_text or '')
    unquoted = unescaped \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace('’', "'")
    normalized = normalize('NFKC', unquoted)

    # Cleaning html markup
    soup = bs(normalized, features='html.parser')
    tags = soup.find_all()
    for tag in tags:
        # Some tags must be removed altogether
        # We remove the tag and all it's content.
        # We alse clear empty tags.
        if tag.name in REMOVABLE_TAGS or not tag.name:
            tag.decompose()

        # Remaining tags must be cleaned
        else:
            if tag.name in allowed_tags:
                attrs = list(tag.attrs.keys())
                for attr in attrs:
                    if attr not in allowed_attrs:
                        tag.attrs.pop(attr)

                # Remove tags with no content
                if not tag.contents and tag.name not in ['br', 'img']:
                    tag.decompose()

                # Remove tags with empty strings (or newlines, etc.)
                elif tag.string and not tag.string.strip():
                    tag.decompose()

            # Some tags are not allowed, but we do not want to remove
            # their content.
            else:
                tag.unwrap()
    prettified = soup.prettify()
    return prettified
