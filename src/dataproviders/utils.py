import csv
from html import unescape
from unicodedata import normalize
from urllib.parse import urljoin

from bs4 import BeautifulSoup as bs

from aids.models import Aid
from categories.models import Theme, Category


REMOVABLE_TAGS = ['script', 'style']
ALLOWED_TAGS = [
    'p', 'ul', 'ol', 'li', 'strong', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'br', 'a', 'iframe',
]
ALLOWED_ATTRS = [
    'href', 'src', 'alt', 'width', 'height', 'style',
    'allow', 'frameborder', 'allowfullscreen',  # to display iframe
    'target', 'rel',  # for links opening in a new tab
]


def content_prettify(raw_text, more_allowed_tags=[], more_allowed_attrs=[], base_url=None):
    """
    Clean imported data.

    We import data from many data sources, and it's not always directly
    usable to say the least. This method performs a list of several
    content beautification so we can safely include ugly data on our site:

     * removes escaped html characters
     * converts weird quote chars and use standard chars instead
     * normalize unicode characters
     * removes all `script` html tags
     * removes most of html tags (but leave their content)
     * removes all html tag attributes
     * replaces relative urls with absolute ones
     * autoindent existing html
    """
    allowed_tags = ALLOWED_TAGS + more_allowed_tags
    allowed_attrs = ALLOWED_ATTRS + more_allowed_attrs

    unescaped = unescape(raw_text or '')
    unquoted = unescaped \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace('’', "'") \
        .replace('target="_blank"', 'target="_blank" rel="noopener"')
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
                if not tag.contents and tag.name not in ['br', 'img', 'iframe']:
                    tag.decompose()

                # Remove tags with empty strings (or newlines, etc.)
                elif tag.string and not tag.string.strip() and tag.name not in ['iframe']:
                    tag.decompose()

                # Replace relative urls with absolute ones
                if tag.name == 'a' and base_url:
                    tag['href'] = urljoin(base_url, tag['href'])

            # Some tags are not allowed, but we do not want to remove
            # their content.
            else:
                tag.unwrap()

    prettified = soup.prettify()

    return prettified


def build_audiences_mapping_dict(audiences_mapping_csv_path, source_column_name='Bénéficiaires', at_column_names=['Bénéficiaires AT']):  # noqa
    """
    Method to extract audiences mapping from a specified csv file
    source audience --> 1 or multiple AT audiences
    """
    audiences_dict = {}

    with open(audiences_mapping_csv_path) as csv_file:
        csvreader = csv.DictReader(csv_file, delimiter=",")
        for index, row in enumerate(csvreader):
            if row[at_column_names[0]]:
                audiences_dict[row[source_column_name]] = []
                for column in at_column_names:
                    if row[column]:
                        try:
                            audience = next(choice[0] for choice in Aid.AUDIENCES if choice[1] == row[column])  # noqa
                            audiences_dict[row[source_column_name]].append(audience)
                        except:  # noqa
                            print('build_audiences_mapping_dict error :', row[column])

    return audiences_dict


def build_categories_mapping_dict(categories_mapping_csv_path, source_column_name='Sous-thématiques', at_column_names=['Sous-thématiques AT']):  # noqa
    """
    Method to extract categories mapping from a specified csv file
    source category --> 1 or multiple AT categories (or theme !)
    """
    categories_dict = {}

    with open(categories_mapping_csv_path) as csv_file:
        csvreader = csv.DictReader(csv_file, delimiter=",")
        for index, row in enumerate(csvreader):
            if row[at_column_names[0]]:
                categories_dict[row[source_column_name]] = []
                for column in at_column_names:
                    if row[column]:
                        category_list = get_category_list_from_name(row[column])
                        categories_dict[row[source_column_name]].extend(category_list)

    return categories_dict


def get_category_list_from_name(category_name):
    """
    Get the corresponding Category object
    (or list of categories if it is a Theme)
    """
    category_list = []

    try:
        category = Category.objects.get(name=category_name)
        category_list.append(category)
    except Category.DoesNotExist:
        # Maybe it's a Theme !
        # If it is, we'll need to add all of its categories
        try:
            theme = Theme.objects.get(name=category_name)
            for category in theme.categories.all():
                category_list.append(category)
        except Theme.DoesNotExist:
            print('build_categories_mapping_dict error :', category_name)

    return category_list


def extract_mapping_values_from_list(mapping_dict, list_of_elems, dict_key=None):
    """
    Source format: list of dicts OR list of strings
    Get the objects, loop on the values and match to the specified mapping dict
    """
    mapping_values = []
    for elem in list_of_elems:
        elem_name = elem.get(dict_key) if dict_key else elem
        if elem_name in mapping_dict:
            mapping_values.extend(mapping_dict.get(elem_name, []))
        else:
            print(f'{elem_name} not mapped')
    return mapping_values
