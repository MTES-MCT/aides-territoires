from django import template

register = template.Library()


PAGINATION_KEY = "page"


@register.simple_tag(takes_context=True)
def querydict(context):
    """Renders the current querydict."""
    querydict = context["request"].GET
    serialized = "?{}".format(querydict.urlencode())
    return serialized


@register.simple_tag(takes_context=True)
def url_to_page(context, page_number):
    """Link to a page without losing existing GET parameters."""

    page_str = "{}".format(page_number)

    querydict = context["request"].GET
    mutable_querydict = querydict.copy()
    mutable_querydict[PAGINATION_KEY] = page_str
    link = "?{}".format(mutable_querydict.urlencode())
    return link
