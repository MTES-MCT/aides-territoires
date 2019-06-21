import factory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory
from bookmarks.models import Bookmark


class BookmarkFactory(DjangoModelFactory):
    class Meta:
        model = Bookmark

    owner = factory.SubFactory(UserFactory)
    querystring = 'text=ademe'
    send_email_alert = True
