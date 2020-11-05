from django.db import models
from django.utils.translation import ugettext_lazy as _


class UploadImage(models.Model):

    image = models.FileField(
        _('Image'),
        upload_to='upload')
    uploaded_at = models.DateTimeField(
        _('Uploaded at'),
        auto_now_add=True)

    class Meta:
        verbose_name = _('Upload image')
        verbose_name_plural = _('Uplad images')

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return self.image.url
