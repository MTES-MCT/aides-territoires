from django.db import models

from geofr.constants import REGIONS, DEPARTMENTS


class RegionField(models.CharField):
    "Model fields to store a single french region."""

    def __init__(self, *args, **kwargs):

        kwargs['max_length'] = kwargs.get('max_length', 2)
        kwargs['choices'] = REGIONS
        super().__init__(*args, **kwargs)


class DepartmentField(models.CharField):
    "Model fields to store a single french department."""

    def __init__(self, *args, **kwargs):

        kwargs['max_length'] = kwargs.get('max_length', 3)
        kwargs['choices'] = DEPARTMENTS
        super().__init__(*args, **kwargs)
