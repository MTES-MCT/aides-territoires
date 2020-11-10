from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.views import View

from upload.models import UploadImage


class UploadImageView(PermissionRequiredMixin, View):
    http_method_names = ['post']
    permission_required = 'is_staff'

    def post(self, request, *args, **kwargs):
        image = self.request.FILES.get('image')
        if not image:
            return JsonResponse({'success': False})
        description = self.request.POST.get('alt', '')
        uploaded = UploadImage.objects.create(
            image=image,
            description=description,
        )
        response_data = {
            'success': True,
            'file': uploaded.image.url,
        }
        return JsonResponse(response_data)
