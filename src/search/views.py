class SearchMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["querystring"] = self.request.GET.urlencode()
        return context
