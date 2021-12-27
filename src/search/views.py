from django.views.generic import FormView

from search.forms import GeneralSearchForm
from geofr.models import Perimeter


class SearchMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['querystring'] = self.request.GET.urlencode()
        return context


class GeneralSearch(FormView):
    """general search form."""

    template_name = 'search/general_search.html'
    form_class = GeneralSearchForm

    def get_initial(self):
        # if user is authenticated
        # and if user organization type and user organization's perimeter are defined
        # we pre-populate targeted_audience & perimeter fields

        if self.request.user.is_authenticated:
            if self.request.user.beneficiary_organization is not None:
                user_org = self.request.user.beneficiary_organization
                if user_org.organization_type is not None and user_org.zip_code:
                    org_zip_code = str(user_org.zip_code).split()
                    org_perimeter = Perimeter.objects.filter(zipcodes=org_zip_code).first()
                    # here we check if zipcode is related to an existing perimeter
                    if org_perimeter:
                        PERIMETER = org_perimeter.id_slug
                        TARGETED_AUDIENCES = user_org.organization_type[0]
                        initial = {
                            'targeted_audiences': TARGETED_AUDIENCES,
                            'perimeter': PERIMETER,
                        }
                        return initial
