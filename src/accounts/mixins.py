from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.conf import settings


class ContributorRequiredMixin(UserPassesTestMixin):
    """Enforce a contributor account.

    If the user is not logged in, redirect to login form.
    If the user is logged in but is not a contributor, redirect to
    the contributor registration form.
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_contributor

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            login_url = settings.LOGIN_URL
        else:
            login_url = 'profile'
        return login_url

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(),
                                 self.get_login_url(),
                                 self.get_redirect_field_name())
