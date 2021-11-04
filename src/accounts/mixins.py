from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login


class UserLoggedRequiredMixin(UserPassesTestMixin):
    """Enforce a user account.

    If the user is not logged in, redirect to login form.
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated

    def get_register_url(self):
        user = self.request.user
        if not user.is_authenticated:
            url = 'register'
        else:
            url = 'home'
        return url

    def get_login_url(self):
        user = self.request.user
        if not user.is_authenticated:
            login_url = settings.LOGIN_URL
        else:
            login_url = 'home'
        return login_url

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(),
                                 self.get_register_url(),
                                 self.get_redirect_field_name())


class ContributorRequiredMixin(UserPassesTestMixin):
    """Enforce a contributor account.

    If the user is not logged in, redirect to login form.
    If the user is logged in and is not a contributor, redirect to home.
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_contributor_or_staff

    def get_register_url(self):
        user = self.request.user
        if not user.is_authenticated:
            url = 'register'
        else:
            url = 'home'
        return url

    def get_login_url(self):
        user = self.request.user
        if not user.is_authenticated:
            login_url = settings.LOGIN_URL
        else:
            login_url = 'home'
        return login_url

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(),
                                 self.get_register_url(),
                                 self.get_redirect_field_name())


class ContributorAndProfileCompleteRequiredMixin(UserPassesTestMixin):
    """Enforce a contributor account.

    If the user is not logged in, redirect to login form.
    If the user is logged in and is not a contributor, redirect to home.
    If the user is logged in and is a contributor but the profile
    is not complete, redirect to the contributor profile form.
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_contributor_or_staff_or_beneficiary and user.bound_to_organization and user.profile_complete  # noqa

    def get_register_url(self):
        user = self.request.user
        if not user.is_authenticated:
            url = 'register'
        else:
            if not user.profile_complete:
                url = 'complete_profile'
            elif not user.bound_to_organization:
                url = 'organization_create_view'
            else:
                url = 'home'
        return url

    def get_login_url(self):
        user = self.request.user
        if not user.is_authenticated:
            login_url = settings.LOGIN_URL
        elif not user.profile_complete:
            login_url = 'complete_profile'
        elif not user.bound_to_organization:
            login_url = 'organization_create_view'
        else:
            if user.is_contributor_or_staff_or_beneficiary:
                login_url = 'organization_create_view'
            else:
                login_url = 'home'
        return login_url

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(),
                                 self.get_register_url(),
                                 self.get_redirect_field_name())
