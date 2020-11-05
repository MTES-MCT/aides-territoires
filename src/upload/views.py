from django.http import JsonResponse
from django.views import View

from .models import UploadImage


class UploadImageView(View):
    http_method_names = ['post']

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
