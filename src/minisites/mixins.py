from aids.models import Aid


class NarrowedFiltersMixin:
    """The minisite feature allows an admin to select the available values for
    some filters such as audiences and categories.

    This mixin provides helpers for such form, where filters are 
    narrowed down to the selection made in the admin site.
    """

    def get_available_categories(self):
        """Return the list of categories available in this minisite.
        Available categories are the one we select in the SearchPage admin
        page.

        When the available categories are defined in the admin, we will
        display them in search form filter.

        There is an initial filtering that applies on the list of aids when
        loading the minisite page. That initial filtering is based on the
        querystring field and is not affected by the selection of available
        categories.
        """
        if not hasattr(self, 'available_categories'):
            page_categories = self.search_page \
                .available_categories \
                .select_related('theme')
            self.available_categories = page_categories
        return self.available_categories

    def get_available_audiences(self):
        """Return the list of audiences available in this minisite."""

        all_audiences = list(Aid.AUDIENCES)
        available_audiences = self.search_page.available_audiences or []
        filtered_audiences = [
            audience for audience in all_audiences
            if audience[0] in available_audiences
        ]
        return filtered_audiences

    def get_form(self, form_class=None):
        """Returns the aid search and filter form."""

        form = super().get_form(form_class)

        # Show available values in categories filter field
        available_categories = self.get_available_categories()
        form.fields['categories'].queryset = available_categories

        # Show available values in the targeted audience filter field
        available_audiences = self.get_available_audiences()
        form.fields['targeted_audiences'].choices = available_audiences

        return form
