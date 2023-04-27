"""Account rendering helpers."""

from django import template


register = template.Library()


@register.simple_tag
def choices_display(obj, field):
    """Choice field rendering"""

    choices = obj._meta.get_field(field).choices
    choices_dict = dict(choices)

    # set to empty list if None
    keys = getattr(obj, field) or []

    return choices_dict.get(keys)


@register.simple_tag(takes_context=True)
def sib_email_id(context):
    """
    Returns the email address if the user is of a type listed in
    target_organization_types.

    Returns an empty string otherwise.
    """
    target_organization_types = [
        "commune",
        "epci",
        "department",
        "public_org",
        "region",
    ]

    result = ""

    user = context["user"]
    if user.is_authenticated and user.beneficiary_organization is not None:
        organization_types = user.beneficiary_organization.organization_type

        # Check overlap between the two lists
        if not set(organization_types).isdisjoint(target_organization_types):
            result = user.email

    return result
