from django.urls import path

from tags.views import TagListView

urlpatterns = [
    path('', TagListView.as_view(), name='tag_list_view'),
]
