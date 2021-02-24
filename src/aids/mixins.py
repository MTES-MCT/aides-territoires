from aids.models import Aid


class AidEditMixin:
    """Common code to aid editing views."""

    def get_queryset(self):
        qs = Aid.objects \
            .filter(author=self.request.user) \
            .select_related('perimeter') \
            .order_by('name')
        self.queryset = qs
        return super().get_queryset()
