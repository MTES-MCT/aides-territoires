from django.views.generic import ListView
from accounts.mixins import ContributorAndProfileCompleteRequiredMixin

from notifications.models import Notification


class NotificationListView(ContributorAndProfileCompleteRequiredMixin, ListView):
    """User notifications dashboard"""

    template_name = "accounts/user_notifications_dashboard.html"
    context_object_name = "notifications"

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)
        return queryset
