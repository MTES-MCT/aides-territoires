from django.shortcuts import redirect


class AdminLiteMixin:
    change_form_template = 'admin/admin_lite/change_form.html'

    def response_change(self, request, obj):
        url = '/'
        if hasattr(self.model, 'get_absolute_url'):
            url = obj.get_absolute_url()
        return redirect(url)
