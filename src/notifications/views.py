from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    DeleteView,
    ListView,
    View,
    UpdateView,
)

from braces.views import MessageMixin

from accounts.mixins import ContributorAndProfileCompleteRequiredMixin
from accounts.models import User
from notifications.forms import NotificationSettingsForm
from notifications.models import Notification


class NotificationListView(ContributorAndProfileCompleteRequiredMixin, ListView):
    """User notifications dashboard"""

    paginate_by = 10
    model = Notification

    template_name = "notifications/notifications_list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        """Only notifications where the user is recipient are available"""
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user).order_by("-date_created")

        return queryset

    def get_context_data(self, **kwargs):
        """Notifications are marked as read when the list page is displayed"""
        context = super().get_context_data(**kwargs)

        unread_notifications = []

        # mark notifications on the current page as read
        current_page_notifications = list(context["object_list"])
        for notification in current_page_notifications:
            if not notification.date_read:
                unread_notifications.append(notification.id)
                notification.mark_as_read()

        context["unread_notifications"] = unread_notifications
        return context


class NotificationDeleteView(
    ContributorAndProfileCompleteRequiredMixin, MessageMixin, DeleteView
):
    """Allow user to delete a notification"""

    model = Notification
    success_url = reverse_lazy("notification_list_view")

    def get_queryset(self):
        # Only allow deletion on own notifications
        qs = Notification.objects.filter(recipient=self.request.user)
        self.queryset = qs
        return super().get_queryset()

    def form_valid(self, form):
        response = super().form_valid(form)
        msg = "Votre notification a été supprimée."
        self.messages.success(msg)
        return response


class NotificationMarkAllReadView(ContributorAndProfileCompleteRequiredMixin, View):
    """Allows user to mark all unread notifications as read"""

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user).order_by("-date_created")

        queryset.update(date_read=timezone.now())

        return HttpResponseRedirect(reverse_lazy("notification_list_view"))


class NotificationDeleteAllView(ContributorAndProfileCompleteRequiredMixin, ListView):
    """Allows user to delete all their notifications"""

    def post(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user).order_by("-date_created")

        queryset.delete()

        return HttpResponseRedirect(reverse("notification_list_view"))


class NotificationSettingsView(
    ContributorAndProfileCompleteRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = NotificationSettingsForm
    template_name = "notifications/settings.html"

    success_message = "Vos préférences ont été mises à jour."

    def get_success_url(self):
        return reverse("notification_list_view")

    def get_object(self):
        return self.request.user
