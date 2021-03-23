from django.urls import path

from blog.views import PostList, PostDetail

urlpatterns = [
    path('', PostList.as_view(), name='post_list_view'),
    path('<slug>', PostDetail.as_view(), name='post_detail_view'),
]
