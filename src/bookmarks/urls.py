from django.urls import path
from django.utils.translation import ugettext_lazy as _

from bookmarks.views import BookmarkList, BookmarkCreate

urlpatterns = [
    path('', BookmarkList.as_view(), name='bookmark_list_view'),
    path(_('create/'), BookmarkCreate.as_view(), name='bookmark_create_view'),
]
