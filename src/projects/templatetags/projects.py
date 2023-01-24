"""Project rendering helpers."""

from django import template


register = template.Library()


@register.simple_tag
def budget_percentage(obj, amount_obtained):
    """Display percentage of the budget represented by the obtained subvention"""
    if obj.budget:
        budget_percentage = (100 * amount_obtained) / obj.budget
        return int(budget_percentage)
