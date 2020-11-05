from django.http import JsonResponse
from django.views import View

from .models import UploadImage


class UploadImageView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        # import ipdb ; ipdb.set_trace()
        image = self.request.FILES['image']
        uploaded = UploadImage.objects.create(image=image)
        response_data = {
            'success': True,
            'file': uploaded.image.url
        }
        return JsonResponse(response_data)
