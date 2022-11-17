class AdminLiteMixin:
    change_form_template = "admin/admin_lite/change_form.html"


class WithViewPermission:
    def has_view_permission(self, request, obj=None):
        """
        Grant permission to authenticated users that are administrator of search pages.
        """
        if (
            request.user.is_authenticated
            and request.user.is_administrator_of_search_pages
        ):
            return True
        return super().has_view_permission(request, obj)


class WithChangePermission(WithViewPermission):
    def has_change_permission(self, request, obj=None):
        """
        Grant permission to authenticated users that are administrator of search pages.
        """
        if (
            request.user.is_authenticated
            and request.user.is_administrator_of_search_pages
        ):
            return True
        return super().has_view_permission(request, obj)


class WithFullPermission(WithChangePermission):
    def has_add_permission(self, request, obj=None):
        """
        Grant permission to authenticated users that are administrator of search pages.
        """
        if (
            request.user.is_authenticated
            and request.user.is_administrator_of_search_pages
        ):
            return True
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """
        Grant permission to authenticated users that are administrator of search pages.
        """
        if (
            request.user.is_authenticated
            and request.user.is_administrator_of_search_pages
        ):
            return True
        return super().has_delete_permission(request, obj)
