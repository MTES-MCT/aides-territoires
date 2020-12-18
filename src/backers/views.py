from django.views.generic import DetailView
from backers.models import Backer


class BackerDetailView(DetailView):
    context_object_name = 'backer'
    template_name = 'backers/detail.html'
    queryset = Backer.objects.all()
