from django.views.generic import RedirectView


class RedirectAidDetailView(RedirectView):
    """
    We are using this view as a temporary fix.
    Some links have been sent to users using the
    wrong aid detail URL (in the PP context) - it was an issue with
    the alert emails.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.get('slug')
        return f'/{slug}/'  # aid_detail_view
