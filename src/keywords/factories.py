import factory
from factory.django import DjangoModelFactory

from keywords.models import SynonymList


class SynonymListFactory(DjangoModelFactory):
    """Factory for synonym-lists."""

    class Meta:
        model = SynonymList

    name = factory.Faker('name')
    keywords_list = factory.Faker('text')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = super()._create(model_class, *args, **kwargs)
        obj.set_search_vector_keywords_list()
        obj.save()
        return obj
