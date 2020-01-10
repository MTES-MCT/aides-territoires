from django.contrib import admin


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
