import factory
from factory.django import DjangoModelFactory

from geofr.models import Perimeter


class PerimeterFactory(DjangoModelFactory):
    """Factory for perimeters."""

    class Meta:
        model = Perimeter

    scale = Perimeter.TYPES.region
    code = factory.Sequence(lambda n: '%08d' % n)
    name = factory.Faker('company')
