from django.urls import path, include

from blog.views import BlogPostList, BlogPostDetail

urlpatterns = [
    path("", BlogPostList.as_view(), name="blog_post_list_view"),
    path("categorie/<category>", BlogPostList.as_view(), name="blog_post_list_view"),
    path(
        "<slug:slug>/",
        include(
            [
                path("", BlogPostDetail.as_view(), name="blog_post_detail_view"),
            ]
        ),
    ),
]
