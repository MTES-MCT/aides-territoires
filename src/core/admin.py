import json

from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import escape
from django.utils.safestring import mark_safe



class InputFilter(admin.SimpleListFilter):
    """Custom django filter with a text input search field.

    See https://hakibenita.com/how-to-add-a-text-filter-to-django-admin
    """

    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name)
        yield all_choice


def pretty_print_readonly_jsonfield(jsonfield_data):
    """
    Display a pretty readonly version of a JSONField
    https://stackoverflow.com/a/60219265
    """

    result = ''

    if jsonfield_data:
        result = json.dumps(jsonfield_data, indent=4, ensure_ascii=False)
        result = mark_safe(f'<pre>{escape(result)}</pre>')

    return result


class AdminLiteMixin:
    change_form_template = 'admin/admin_lite/change_form.html'

    def response_change(self, request, obj):
        url = '/'
        if hasattr(self.model, 'get_absolute_url'):
            url = obj.get_absolute_url()
        return redirect(url)
