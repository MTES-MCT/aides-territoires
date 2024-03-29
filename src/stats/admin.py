from django.contrib import admin

from core.admin import pretty_print_readonly_jsonfield
from stats.models import (
    AidCreateDSFolderEvent,
    AccountRegisterFromNextpagewarningClickEvent,
    AidSearchEvent,
    AidViewEvent,
    AidContactClickEvent,
    AidOriginUrlClickEvent,
    AidApplicationUrlClickEvent,
    AidEligibilityTestEvent,
    BackerViewEvent,
    ContactFormSendEvent,
    Event,
    PostViewEvent,
    ProgramViewEvent,
    PromotionClickEvent,
    PromotionDisplayEvent,
    PublicProjectViewEvent,
    PublicProjectSearchEvent,
    ValidatedProjectSearchEvent,
)


class AidCreateDSFolderEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "aid", "date_created"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AccountRegisterFromNextpagewarningClickEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "date_created"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AidViewEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "aid", "source", "date_created"]
    list_filter = ["source"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AidContactClickEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "aid", "source", "date_created"]
    list_filter = ["source"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AidOriginUrlClickEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "aid", "source", "date_created"]
    list_filter = ["source"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AidApplicationUrlClickEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "aid", "source", "date_created"]
    list_filter = ["source"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AidSearchEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "source", "results_count", "date_created"]
    list_filter = ["source"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AidEligibilityTestEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = [
        "id",
        "aid",
        "eligibility_test",
        "answer_success",
        "source",
        "date_created",
    ]
    list_filter = ["eligibility_test", "source"]
    readonly_fields = ["get_pprint_answer_details"]

    def get_pprint_answer_details(self, obj=None):
        if obj:
            return pretty_print_readonly_jsonfield(obj.answer_details)
        return ""

    get_pprint_answer_details.short_description = "Answer details (pretty)"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BackerViewEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "backer", "source", "date_created"]
    list_filter = ["source"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PostViewEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "post", "date_created"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ProgramViewEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "program", "source", "date_created"]
    list_filter = ["source"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PromotionDisplayEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "promotion", "querystring", "source", "date_created"]
    list_filter = ["source"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PromotionClickEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "promotion", "querystring", "source", "date_created"]
    list_filter = ["source"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ContactFormSendEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "subject", "date_created"]
    list_filter = ["subject"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EventAdmin(admin.ModelAdmin):
    """The model is set to (almost) readonly"""

    list_display = ["category", "event", "meta", "source", "value", "date_created"]
    list_filter = ["category", "event", "source"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PublicProjectViewEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "project", "date_created"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ValidatedProjectSearchEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "date_created"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PublicProjectSearchEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ["id", "date_created"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(AidCreateDSFolderEvent, AidCreateDSFolderEventAdmin)
admin.site.register(
    AccountRegisterFromNextpagewarningClickEvent,
    AccountRegisterFromNextpagewarningClickEventAdmin,
)
admin.site.register(AidViewEvent, AidViewEventAdmin)
admin.site.register(AidContactClickEvent, AidContactClickEventAdmin)
admin.site.register(AidOriginUrlClickEvent, AidOriginUrlClickEventAdmin)
admin.site.register(AidApplicationUrlClickEvent, AidApplicationUrlClickEventAdmin)
admin.site.register(AidSearchEvent, AidSearchEventAdmin)
admin.site.register(AidEligibilityTestEvent, AidEligibilityTestEventAdmin)
admin.site.register(BackerViewEvent, BackerViewEventAdmin)
admin.site.register(ContactFormSendEvent, ContactFormSendEventAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(PostViewEvent, PostViewEventAdmin)
admin.site.register(ProgramViewEvent, ProgramViewEventAdmin)
admin.site.register(PromotionDisplayEvent, PromotionDisplayEventAdmin)
admin.site.register(PromotionClickEvent, PromotionClickEventAdmin)
admin.site.register(PublicProjectViewEvent, PublicProjectViewEventAdmin)
admin.site.register(PublicProjectSearchEvent, PublicProjectSearchEventAdmin)
admin.site.register(ValidatedProjectSearchEvent, ValidatedProjectSearchEventAdmin)
