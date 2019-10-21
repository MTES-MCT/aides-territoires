from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _, ugettext
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from braces.views import MessageMixin

from bookmarks.forms import BookmarkAlertForm, UserBookmarkForm
from bookmarks.models import Bookmark


class BookmarkMixin:

    def get_queryset(self):
        qs = Bookmark.objects \
            .filter(owner=self.request.user) \
            .order_by('-date_created')
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
        return UserBookmarkForm(self.request.POST)

    def form_valid(self, form):

        # Extract search parameters and exclude the bookmark
        # configuration fields.
        post_data = self.request.POST.copy()
        post_data.pop('title')
        post_data.pop('send_email_alert', None)
        querystring = post_data.urlencode()

        # Create the bookmark object
        Bookmark.objects.create(
            owner=self.request.user,
            title=form.cleaned_data['title'],
            send_email_alert=form.cleaned_data['send_email_alert'],
            querystring=querystring)

        bookmarks_url = reverse('bookmark_list_view')
        message = _('Your new bookmark was successfully created. '
                    '<a href="%(url)s">You will find in in your bookmark '
                    'list.</a>') % {'url': bookmarks_url}
        self.messages.success(message)
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


class BookmarkUpdate(LoginRequiredMixin, MessageMixin, BookmarkMixin,
                     UpdateView):

    form_class = BookmarkAlertForm
    http_method_names = ['post']
    success_url = reverse_lazy('bookmark_list_view')
    success_message = _('The email notification settings was updated.')

    def form_valid(self, form):
        """Handles the update response.

        This view is meant to be called via ajax, but must also work with
        a regular POST call, because progressive enhancement.
        """
        response = super().form_valid(form)
        if self.request.is_ajax():
            response = HttpResponse()
        else:
            self.messages.success(self.success_message)
        return response
