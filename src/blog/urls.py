from django.urls import path, include

from blog.views import PostList, PostListCategory, PostDetail

urlpatterns = [
    path('', PostList.as_view(), name='post_list_view'),
    path('category/', PostListCategory.as_view(),
         name='post_list_category_view'),

    path('<slug:slug>/', include([
        path('', PostDetail.as_view(), name='post_detail_view'),
    ])),
]
