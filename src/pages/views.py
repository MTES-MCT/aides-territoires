from django.views.generic import DetailView
from django.urls import reverse
from django.http import Http404, HttpResponsePermanentRedirect
from django.core.exceptions import PermissionDenied

from pages.models import Page


class PageView(DetailView):
    context_object_name = "page"
    template_name = "pages/detail.html"

    def get(self, request, *args, **kwargs):
        url = self.kwargs.get("url")
        if "://" in url:
            raise PermissionDenied()
        elif url == "europe/":
            redirect_url = reverse("search_page", args=["europe"])
            return HttpResponsePermanentRedirect(redirect_url)
        elif not url.endswith("/"):
            return HttpResponsePermanentRedirect(f"{url}/")
        return super().get(request, *args, **kwargs)

    def get_object(self):
        url = self.kwargs.get("url")
        if not url.startswith("/"):
            url = f"/{url}"

        try:
            page = Page.objects.get(url=url)
        except Page.DoesNotExist:
            raise Http404("No page found")

        return page
