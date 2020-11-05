from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import UploadImageView


urlpatterns = [
    path('', csrf_exempt(UploadImageView.as_view()), name='upload_image'),
]
