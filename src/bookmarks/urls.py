from django.urls import path, include
from django.utils.translation import ugettext_lazy as _

from bookmarks.views import BookmarkList, BookmarkCreate, BookmarkDelete

urlpatterns = [
    path('', BookmarkList.as_view(), name='bookmark_list_view'),
    path(_('create/'), BookmarkCreate.as_view(), name='bookmark_create_view'),
    path('<int:pk>/', include([
        path(_('delete/'), BookmarkDelete.as_view(),
             name='bookmark_delete_view'),
    ]))
]
