from django_otp.admin import OTPAdminSite as BaseOTPAdminSite


class OTPAdminSite(BaseOTPAdminSite):

    def can_bypass_otp(self, request):
        """
        We bypass OTP for non-super user's that are administrator
        of search pages.
        """
        can_bypass_otp = request.user.is_authenticated and \
            not request.user.is_superuser and \
            request.user.is_administrator_of_search_pages
        return can_bypass_otp

    def has_permission(self, request):
        if self.can_bypass_otp(request):
            return True
        return super().has_permission(request)
