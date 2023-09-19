from django.contrib.admin.filters import AllValuesFieldListFilter


class DropdownFilter(AllValuesFieldListFilter):
    template = "admin/dropdown_filter.html"
