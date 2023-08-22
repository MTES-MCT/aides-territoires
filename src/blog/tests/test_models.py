import pytest
from blog.factories import BlogPostFactory

from blog.models import BlogPostCategory, logo_upload_to, promotion_img_upload_to

pytestmark = pytest.mark.django_db


def test_logo_upload_to():
    post = BlogPostFactory(title="Champignac devient un village moderne")

    result = logo_upload_to(post, "0345.png")

    assert result == "blog/champignac-devient-un-village-moderne_logo.png"


def test_promotion_img_upload_to():
    post = BlogPostFactory(title="Champignac devient un village moderne")

    result = promotion_img_upload_to(post, "123.jpeg")

    assert result == "promotion/champignac-devient-un-village-moderne_img.jpeg"


def test_blog_post_publication_sets_date():
    post = BlogPostFactory(status="published")

    assert post.date_published is not None


def test_blog_post_category():
    cat = BlogPostCategory(name="Articles")
    cat.save()

    assert cat.get_absolute_url() == "/blog/categorie/articles"
