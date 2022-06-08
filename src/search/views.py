from django.views.generic import FormView

from search.forms import GeneralSearchForm


class SearchMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["querystring"] = self.request.GET.urlencode()
        return context


class GeneralSearch(FormView):
    """general search form."""

    template_name = "search/general_search.html"
    form_class = GeneralSearchForm

    def get_initial(self):
        # if user is authenticated
        # and if user organization type and user organization's perimeter are defined
        # we pre-populate targeted_audience & perimeter fields

        if self.request.user.is_authenticated:
            if self.request.user.beneficiary_organization is not None:
                TARGETED_AUDIENCES = None
                PERIMETER = None
                user_org = self.request.user.beneficiary_organization
                if user_org.organization_type is not None:
                    TARGETED_AUDIENCES = user_org.organization_type[0]
                if user_org.perimeter is not None:
                    PERIMETER = user_org.perimeter.id_slug
                initial = {
                    "targeted_audiences": TARGETED_AUDIENCES,
                    "perimeter": PERIMETER,
                }
                return initial
