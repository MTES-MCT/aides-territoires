import re
from django.views.generic import DetailView
from django.http import Http404, HttpResponsePermanentRedirect
from pages.models import Page


class PageView(DetailView):
    context_object_name = "page"
    template_name = "pages/detail.html"

    def get(self, request, *args, **kwargs):
        url = self.kwargs.get("url")

        if re.match("[A-Za-z0-9_À-ÿ/-]+", url) and not url.endswith("/"):
            return HttpResponsePermanentRedirect(url + "/")
        return super().get(request, *args, **kwargs)

    def get_object(self):
        url = self.kwargs.get("url")
        if not url.startswith("/"):
            url = "/" + url

        try:
            page = Page.objects.get(url=url)
        except Page.DoesNotExist:
            raise Http404("No page found")

        return page
