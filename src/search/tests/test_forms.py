from search.models import SearchPage
from search.forms import SearchPageAdminForm


# Model forms for admin modules cannot be configured with the usual
# `model` and `exclude` Meta settings, which makes the form impossible to
# instanciate directly. Thus, we override it to make easier to test.
class DummySearchPageAdminForm(SearchPageAdminForm):
    class Meta:
        model = SearchPage
        exclude = ["date_created", "date_updated"]


CONTACT_LINK = "https://aides-territoires.beta.gouv.fr/contact/"


def test_valid_search_page_form():
    form = DummySearchPageAdminForm(
        {
            "title": "Test title",
            "slug": "test-title",
            "contact_link": CONTACT_LINK,
            "content": "Test content",
            "more_content": "Test content",
            "search_querystring": "text=",
            "show_perimeter_field": True,
            "show_audience_field": True,
            "show_categories_field": True,
            "show_mobilization_step_field": False,
            "show_aid_type_field": False,
            "show_backers_field": False,
        }
    )

    assert form.is_valid()


def test_search_form_field_customizations():
    """It's possible to hide some search form fields."""

    form = DummySearchPageAdminForm(
        {
            "title": "Test title",
            "slug": "test-title",
            "contact_link": CONTACT_LINK,
            "content": "Test content",
            "more_content": "Test content",
            "search_querystring": "text=",
            "show_perimeter_field": True,
            "show_audience_field": False,
            "show_categories_field": False,
            "show_mobilization_step_field": False,
            "show_aid_type_field": False,
            "show_backers_field": False,
        }
    )

    assert form.is_valid()


def test_search_form_not_enough_filters():
    """It's impossible to hide *all* search form fields."""

    form = DummySearchPageAdminForm(
        {
            "title": "Test title",
            "slug": "test-title",
            "contact_link": CONTACT_LINK,
            "content": "Test content",
            "more_content": "Test content",
            "search_querystring": "text=",
            "show_perimeter_field": False,
            "show_audience_field": False,
            "show_categories_field": False,
            "show_mobilization_step_field": False,
            "show_aid_type_field": False,
            "show_backers_field": False,
        }
    )

    assert not form.is_valid()
    assert form.errors.as_data()["__all__"][0].code == "not_enough_filters"


def test_search_form_too_many_filters():
    """It's impossible to select more than three search form fields."""

    form = DummySearchPageAdminForm(
        {
            "title": "Test title",
            "slug": "test-title",
            "contact_link": CONTACT_LINK,
            "content": "Test content",
            "more_content": "Test content",
            "search_querystring": "text=",
            "show_perimeter_field": True,
            "show_audience_field": True,
            "show_categories_field": True,
            "show_mobilization_step_field": True,
            "show_aid_type_field": True,
            "show_backers_field": True,
        }
    )

    assert not form.is_valid()
    assert form.errors.as_data()["__all__"][0].code == "too_many_filters"
