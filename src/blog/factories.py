import factory
from factory.django import DjangoModelFactory


from blog.models import BlogPost


class BlogPostFactory(DjangoModelFactory):
    """Factory for blog post."""

    class Meta:
        model = BlogPost

    title = factory.Faker("company")
    text = factory.Faker("text", locale="fr_FR")
