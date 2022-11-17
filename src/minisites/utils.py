from core.utils import RedirectAidDetailView as BaseRedirectAidDetailView


class RedirectAidDetailView(BaseRedirectAidDetailView):
    redirect_url = "/{slug}/"
