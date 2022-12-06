from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy

from accounts.mixins import ContributorAndProfileCompleteRequiredMixin

from notifications.models import Notification
from braces.views import MessageMixin


class NotificationListView(ContributorAndProfileCompleteRequiredMixin, ListView):
    """User notifications dashboard"""

    template_name = "accounts/user_notifications_dashboard.html"
    context_object_name = "notifications"

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)
        return queryset


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
