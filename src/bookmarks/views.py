from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from braces.views import MessageMixin

from accounts.forms import RegisterForm
from accounts.models import User
from bookmarks.tasks import send_alert_confirmation_email
from bookmarks.forms import (BookmarkAlertForm, UserBookmarkForm,
                             AnonymousBookmarkForm)
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


class BookmarkCreate(MessageMixin, BookmarkMixin, CreateView):
    """Create a bookmark by saving a search view querystring.

    This view has to handle four cases:

     1. the user creating the bookmark is already connected.
     2. the user is just an anonymous visitor.
     3. the user is an anonymous visitor but they already created a
        bookmark with the same email address.
     4. the user isn't logged in but their email correspond to a known and
        valid account.

    """

    http_method_names = ['post']

    def get_form(self):
        if self.request.user.is_authenticated:
            BookmarkForm = UserBookmarkForm
        else:
            BookmarkForm = AnonymousBookmarkForm

        return BookmarkForm(self.request.POST)

    @transaction.atomic
    def form_valid(self, form):

        if self.request.user.is_authenticated:
            user_email = self.request.user.email
        else:
            user_email = form.cleaned_data['email']

        try:
            existing_account = User.objects.get(email=user_email)
        except User.DoesNotExist:
            existing_account = None

        if existing_account:
            owner = existing_account
            send_alert = form.cleaned_data.get('send_email_alert', True)
            bookmark = self.create_bookmark(form, owner, send_alert)
            bookmarks_url = reverse('bookmark_list_view')
            message = _('Your new bookmark was successfully created. '
                        '<a href="%(url)s">You will find in in your bookmark '
                        'list.</a>') % {'url': bookmarks_url}

        else:
            owner = self.create_account(form)
            send_alert = True
            bookmark = self.create_bookmark(form, owner, send_alert)
            send_alert_confirmation_email.delay(owner.email, bookmark.id)
            message = _('We just sent you an email to validate your address.')

        self.messages.success(message)
        redirect_url = reverse('search_view')
        return HttpResponseRedirect('{}?{}'.format(
            redirect_url, bookmark.querystring))

    def create_bookmark(self, form, owner, send_alert):
        """Create a new bookmark."""

        bookmark = Bookmark.objects.create(
            owner=owner,
            title=form.cleaned_data['title'],
            send_email_alert=send_alert,
            alert_frequency=form.cleaned_data['alert_frequency'],
            querystring=form.cleaned_data['querystring'])

        return bookmark

    def create_account(self, form):
        """Create a tmp account to attach the bookmark to."""

        register_form = RegisterForm({
            'email': form.cleaned_data['email'],
            'full_name': form.cleaned_data['email'],
            'ml_consent': False})
        user = register_form.save()
        return user

    def form_invalid(self, form):
        if form.has_error("email", "unique"):
            msg = "Un compte avec cette adresse existe déjà. Avez-vous oublié de vous connecter ?"
        else:
            msg = _('We could not create your bookmark because of those '
                    'errors: {}').format(form.errors.as_text())

        self.messages.error(msg)
        redirect_url = reverse('search_view')
        return HttpResponseRedirect(redirect_url)


class BookmarkDelete(LoginRequiredMixin, MessageMixin, BookmarkMixin,
                     DeleteView):
    success_url = reverse_lazy('bookmark_list_view')

    def delete(self, *args, **kwargs):
        res = super().delete(*args, **kwargs)
        self.messages.success(_('Your bookmark was deleted.'))
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
