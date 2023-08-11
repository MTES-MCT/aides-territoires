import pytest

from django.urls import reverse

from blog.factories import BlogPostFactory

pytestmark = pytest.mark.django_db


def test_user_can_view_post_list(client):
    blog_post = BlogPostFactory(status="published")

    blog_post_list = reverse("blog_post_list_view")
    res = client.get(blog_post_list)
    assert blog_post.title in res.content.decode()


def test_anonymous_user_can_view_published_blog_post(client):
    blog_post = BlogPostFactory(status="published")
    blog_post_detail_url = reverse("blog_post_detail_view", args=[blog_post.slug])
    res = client.get(blog_post_detail_url)
    assert res.status_code == 200


def test_connected_user_can_view_published_blog_post(client, user):
    client.force_login(user)
    blog_post = BlogPostFactory(status="published")
    blog_post_detail_url = reverse("blog_post_detail_view", args=[blog_post.slug])
    res = client.get(blog_post_detail_url)
    assert res.status_code == 200


def test_user_without_superuser_status_can_not_view_draft_blog_post(client, user):
    """Classic user (not superuser) can not previewed draft blogpost."""

    client.force_login(user)
    blog_post = BlogPostFactory(status="draft")
    blog_post_detail_url = reverse("blog_post_detail_view", args=[blog_post.slug])
    res = client.get(blog_post_detail_url)
    assert res.status_code == 404


def test_super_user_can_previewed_draft_blogpost(client, superuser):
    """Only superuser can previewed draft blogpost."""

    client.force_login(superuser)
    blog_post = BlogPostFactory(status="draft")
    blog_post_detail_url = reverse("blog_post_detail_view", args=[blog_post.slug])
    res = client.get(blog_post_detail_url)
    assert res.status_code == 200
    assert (
        "Cet article n’est actuellement pas affiché sur le site."
        in res.content.decode()
    )
