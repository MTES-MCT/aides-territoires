from django.views.generic import DetailView
from django.db.models import Prefetch

from backers.models import Backer
from aids.models import Aid
from categories.models import Category

class BackerDetailView(DetailView):
    context_object_name = 'backer'
    template_name = 'backers/detail.html'
    queryset = Backer.objects.all()

    def get_context_data(self, **kwargs):

        categories_list = Category.objects \
            .select_related('theme') \

        aids = Aid.objects.open().published() \
            .filter(financers=self.object.id) \
            .prefetch_related(Prefetch('categories', queryset=categories_list))

        list_themes = {}
        for aid in aids:
            for category in aid.categories.all():
                list_themes[category] = category.theme
        themes = set(list_themes.values())

        categories_by_theme = {}
        for theme in themes:
            categories_by_theme[theme] = [k for k in list_themes.keys() if list_themes[k] == theme]

        programs = Aid.objects.open().published() \
            .filter(financers=self.object.id) \
            .filter(programs=True)

        context = super().get_context_data(**kwargs)
        context['aids'] = aids
        context['categories_by_theme'] = categories_by_theme
        context['programs'] = programs

        return context