import factory
from factory.django import DjangoModelFactory

from geofr.models import Perimeter


class PerimeterFactory(DjangoModelFactory):
    """Factory for perimeters."""

    class Meta:
        model = Perimeter
        django_get_or_create = ("scale", "code")

    scale = Perimeter.SCALES.region
    code = factory.Sequence(lambda n: "%08d" % n)
    name = factory.Faker("company")

    @factory.post_generation
    def contained_in(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for perimeter in extracted:
                self.contained_in.add(perimeter)
