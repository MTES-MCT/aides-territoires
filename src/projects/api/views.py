import operator
from functools import reduce
from rest_framework import viewsets
from django.db.models import Q

from projects.models import Project
from projects.api.serializers import ProjectSerializer


MIN_SEARCH_LENGTH = 3


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Filter data according to search query."""

        qs = Project.objects.all()

        q = self.request.query_params.get('q', '')
        terms = q.split()
        q_filters = []
        for term in terms:
            if len(term) >= MIN_SEARCH_LENGTH:
                q_filters.append(Q(key_words__icontains=term))
        if q_filters:
            qs = qs.filter(reduce(operator.and_, q_filters))

        is_published = self.request.query_params.get('is_published', 'false')  # noqa
        if is_published == 'true':
            qs = qs.filter(status="published")

        categories = self.request.query_params.get('categories[]', '')
        categories_term = categories.split(", ")
        categories_filters = []
        for category_term in categories_term:
            categories_filters.append(Q(categories__name=category_term))
        if categories_filters:
            qs = qs.filter(reduce(operator.and_, categories_filters))


        qs = qs.order_by('name')

        return qs
