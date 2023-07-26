import csv
import emoji
from html import unescape
from bs4 import BeautifulSoup as bs
import re
from unicodedata import normalize
from urllib.parse import urljoin

from aids.models import Aid
from categories.models import Theme, Category


REMOVABLE_TAGS = ["script", "style"]
ALLOWED_TAGS = [
    "p",
    "span",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "br",
    "a",
    "table",
    "caption",
    "tbody",
    "tr",
    "td",
    "th",
    "iframe",
    "figcaption",
    "figure",
    "video",
    "source",
]
ALLOWED_ATTRS = [
    "href",
    "src",
    "alt",
    "style",
    "class",
    "allow",
    "title",
    "scope",  # for tables
    "allowfullscreen",  # to display iframe
    "target",
    "aria-hidden",
    "rel",  # for links opening in a new tab
    "controls",  # for the video tag
    "poster",  # for the video tag
    "preload",  # for the video tag
    "type",  # for the source tag
]


def content_prettify(
    raw_text, more_allowed_tags=[], more_allowed_attrs=[], base_url=None
):
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

    unescaped = unescape(raw_text or "")

    unquoted = (
        unescaped.replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace('target="_blank"', 'target="_blank" rel="noopener"')
    )
    normalized = normalize("NFKC", unquoted)

    # Cleaning html markup
    soup = bs(normalized, features="html.parser")
    tags = soup.find_all()
    for tag in tags:
        # Some tags must be removed altogether
        # We remove the tag and all it's content.
        # We alse clear empty tags.
        if tag.name in REMOVABLE_TAGS or not tag.name:
            tag.decompose()

        # Remaining tags must be cleaned
        else:
            clean_tag(tag, allowed_tags, allowed_attrs, base_url, soup)

    prettified = soup.prettify()

    emojified = mark_emojis(prettified)

    return emojified


def clean_tag(tag, allowed_tags, allowed_attrs, base_url, soup):
    if tag.name in allowed_tags:
        clean_attrs(tag, allowed_attrs)

        # Remove tags with no content
        # or with empty strings (or newlines, etc.)
        if (
            not tag.contents
            and tag.name
            not in [
                "br",
                "img",
                "iframe",
                "source",
            ]
        ) or (
            tag.string
            and not tag.string.strip()
            and tag.name
            not in [
                "iframe",
                "source",
            ]
        ):
            tag.decompose()

        # Replace relative urls with absolute ones
        if tag.name == "a":
            clean_link_tag(tag, base_url, soup)

        if tag.name == "iframe":
            clean_iframe_tag(tag, soup)
    # Some tags are not allowed, but we do not want to remove
    # their content.
    else:
        tag.unwrap()

    return tag


def clean_attrs(tag, allowed_attrs):
    attrs = list(tag.attrs.keys())
    for attr in attrs:
        if attr not in allowed_attrs:
            tag.attrs.pop(attr)


def clean_iframe_tag(tag, soup):
    """
    Makes some transformations on iframes containing Youtube videos
    """
    if "youtube.com" in tag.attrs["src"]:
        tag.attrs["class"] = "at-youtube-video"

        wrapper_attrs = {"class": "at-responsive-video"}
        if tag.parent.attrs != wrapper_attrs:
            wrapper = soup.new_tag("div")
            wrapper.attrs = wrapper_attrs
            tag.wrap(wrapper)


def clean_link_tag(tag, base_url, soup):
    if base_url:
        tag["href"] = urljoin(base_url, tag["href"])

    # Add a warning for screenreaders on external links
    if "target" in tag.attrs and tag.attrs["target"] == "_blank":
        target_warning = soup.new_tag("span")
        target_warning.attrs = {"class": "fr-sr-only"}
        target_warning.string = "Ouvre une nouvelle fenêtre"
        if "Ouvre une nouvelle fenêtre" not in tag.text:
            tag.append(target_warning)


def mapping_audiences(audiences_mapping_csv_path, source_column_name, at_column_names):
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
                            audience = next(
                                choice[0]
                                for choice in Aid.AUDIENCES
                                if choice[1] == row[column]
                            )  # noqa
                            audiences_dict[row[source_column_name]].append(audience)
                        except Exception:
                            print(row[column])

    return audiences_dict


def mapping_categories(
    categories_mapping_csv_path, source_column_name, at_column_names
):
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
            print(category_name)

    return category_list


def mapping_categories_label(
    categories_mapping_csv_path, source_column_name, source_column_label
):
    """
    Method to extract category label from a specified category code
    """

    categories_label_dict = {}

    with open(categories_mapping_csv_path) as csv_file:
        csvreader = csv.DictReader(csv_file, delimiter=",")
        for index, row in enumerate(csvreader):
            if row[source_column_label]:
                categories_label_dict[row[source_column_name]] = row[
                    source_column_label
                ]
    return categories_label_dict


def add_emoji_span(emoji: str, data_dict: dict) -> str:
    """Wraps an emoji in a span with the aria-hidden attr"""
    return f'<span aria-hidden="true">{emoji}</span>'


def mark_emojis(text_string: str) -> str:
    """Parse a string to add a span to emojis"""
    marked_string = emoji.replace_emoji(text_string, add_emoji_span)

    # Subsequent saves of the page should not result in multiple imbricated spans
    double_spans = r"<span aria-hidden=\"true\">\s*<span aria-hidden=\"true\">(?P<emoji>.*)</span>\s*</span>"  # noqa
    return re.sub(
        double_spans, r'<span aria-hidden="true">\g<emoji></span>', marked_string
    )
