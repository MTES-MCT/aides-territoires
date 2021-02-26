from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.http import HttpResponseRedirect
from braces.views import MessageMixin

from projects.forms import ProjectSuggestForm
from categories.models import Category


class ProjectSuggest(MessageMixin, CreateView):
    """Allows users to suggest their own projects."""

    template_name = 'search/step_project.html'
    form_class = ProjectSuggestForm
    context_object_name = 'project'

    def form_valid(self, form):

        querystring = self.request.GET.urlencode()
        categories_list = self.request.GET.getlist('categories', '')
        categories = Category.objects \
            .filter(slug__in=categories_list) \
            .values_list('id', flat=True)

        project = form.save(commit=False)
        project.is_suggested = True

        project.save()
        form.save_m2m()
        project.categories.add(*categories)

        msg = _('Thank you for contributing !')
        self.messages.success(msg)
        url = reverse('search_view')
        url = '{}?{}'.format(url, querystring)
        return HttpResponseRedirect(url)
