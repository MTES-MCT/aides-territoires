"""Project rendering helpers."""
from math import acos, cos, radians, sin
from django import template


register = template.Library()


@register.simple_tag
def budget_percentage(obj, amount_obtained):
    """Display percentage of the budget represented by the obtained subvention"""
    if obj.budget:
        budget_percentage = (100 * amount_obtained) / obj.budget
        return int(budget_percentage)


@register.simple_tag
def distance_between_two_perimeters(perimeter_1, perimeter_2):
    print(perimeter_1)
    distance = (
        acos(
            cos(radians(perimeter_1.latitude))
            * cos(radians(perimeter_2.latitude))
            * cos(radians(perimeter_2.longitude) - radians(perimeter_1.longitude))
            + sin(radians(perimeter_1.latitude)) * sin(radians(perimeter_2.latitude))
        )
        * 6371
    )
    return round(distance)
