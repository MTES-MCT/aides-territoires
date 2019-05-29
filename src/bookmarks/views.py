from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from braces.views import MessageMixin

from bookmarks.models import Bookmark
from aids.forms import AidSearchForm


class BookmarkMixin:
    def get_queryset(self):
        qs = Bookmark.objects \
            .filter(owner=self.request.user) \
            .order_by('date_created')
        return qs


class BookmarkList(LoginRequiredMixin, BookmarkMixin, ListView):
    template_name = 'bookmarks/list.html'
    context_object_name = 'bookmarks'


@method_decorator(csrf_exempt, name='dispatch')
class BookmarkCreate(LoginRequiredMixin, MessageMixin, BookmarkMixin,
                     CreateView):
    """Create a bookmark by saving a search view querystring.

    Note: the search form, by default, uses the GET method. Hence, we
    don't pass the form a csrf token and that's why we had to exempt this
    view from csrf protection.
    """

    http_method_names = ['post']

    def get_form(self):
        return AidSearchForm(self.request.POST)

    def form_valid(self, form):
        querystring = self.request.POST.urlencode()
        Bookmark.objects.create(
            owner=self.request.user, querystring=querystring)
        self.messages.success(_('Your new bookmark was successfully created.'))
        redirect_url = reverse('search_view')
        return HttpResponseRedirect('{}?{}'.format(redirect_url, querystring))

    def form_invalid(self, form):
        self.messages.error(_('Something went wrong. Please try again.'))
        redirect_url = reverse('search_view')
        return HttpResponseRedirect(redirect_url)


class BookmarkDelete(LoginRequiredMixin, MessageMixin, BookmarkMixin,
                     DeleteView):
    success_url = reverse_lazy('bookmark_list_view')

    def delete(self, *args, **kwargs):
        res = super().delete(*args, **kwargs)
        self.messages.success('Your bookmark was deleted.')
        return res
