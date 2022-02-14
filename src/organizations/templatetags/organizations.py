"""Organization rendering helpers."""

from django import template
from organizations.models import Organization

register = template.Library()


@register.simple_tag
def Organization_type_choice_display(choice):
    organization_type = Organization._meta.get_field('organization_type').base_field
    organization_type = organization_type.choices
    return organization_type[choice]
