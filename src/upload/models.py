from django.db import models


class UploadImage(models.Model):
    image = models.FileField("Image", upload_to="upload")
    description = models.CharField(
        "Description", max_length=180, blank=True, default=""
    )
    uploaded_at = models.DateTimeField("Uploadé à", auto_now_add=True)

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return self.image.url
