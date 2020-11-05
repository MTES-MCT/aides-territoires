from django.db import models
from django.utils.translation import ugettext_lazy as _


class UploadImage(models.Model):

    image = models.FileField(
        _('Image'),
        upload_to='upload')
    description = models.CharField(
        _('Description'),
        max_length=180,
        blank=True, default='')
    uploaded_at = models.DateTimeField(
        _('Uploaded at'),
        auto_now_add=True)

    class Meta:
        verbose_name = _('Upload image')
        verbose_name_plural = _('Upload images')

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return self.image.url
