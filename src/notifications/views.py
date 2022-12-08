from django.views.generic import ListView, DeleteView, DetailView
from django.urls import reverse_lazy

from accounts.mixins import ContributorAndProfileCompleteRequiredMixin

from notifications.models import Notification
from braces.views import MessageMixin


class NotificationListView(ContributorAndProfileCompleteRequiredMixin, ListView):
    """User notifications dashboard"""

    template_name = "notifications/notifications_list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        """Only notifications where the user is recipient are available"""
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user).order_by("-date_created")

        return queryset


class NotificationDetailView(ContributorAndProfileCompleteRequiredMixin, DetailView):
    """User notifications dashboard"""

    template_name = "notifications/notification_detail.html"
    context_object_name = "notifications"

    def get_queryset(self):
        # Only allow own notifications
        qs = Notification.objects.filter(recipient=self.request.user)
        self.queryset = qs
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Notifications are marked as read when the list page is displayed"""
        context = super().get_context_data(**kwargs)

        self.object.mark_as_read()

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

    def delete(self, *args, **kwargs):
        res = super().delete(*args, **kwargs)
        msg = "Votre notification a été supprimée."
        self.messages.success(msg)
        return res
