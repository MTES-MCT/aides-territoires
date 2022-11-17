from django.contrib import admin

from upload.models import UploadImage


@admin.register(UploadImage)
class UploadImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "description", "uploaded_at"]
    date_hierarchy = "uploaded_at"
