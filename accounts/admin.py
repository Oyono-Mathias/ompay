from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from .models import User, KycRequest

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Infos OM Pay", {"fields": ("phone_number", "country")}),
    )
    list_display = ("username", "email", "phone_number", "is_staff")

@admin.action(description="Approuver les KYC sélectionnés")
def approve_selected(modeladmin, request, queryset):
    for k in queryset:
        k.status = KycRequest.APPROVED
        k.reviewed_at = timezone.now()
        k.reviewed_by = request.user
        k.save()

@admin.action(description="Refuser les KYC sélectionnés")
def reject_selected(modeladmin, request, queryset):
    for k in queryset:
        k.status = KycRequest.REJECTED
        k.reviewed_at = timezone.now()
        k.reviewed_by = request.user
        if not k.review_notes:
            k.review_notes = "Refusé par l'admin."
        k.save()

@admin.register(KycRequest)
class KycRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "doc_type", "status", "created_at", "reviewed_at", "reviewed_by")
    list_filter = ("status", "doc_type", "created_at")
    search_fields = ("user__username", "id_number")
    actions = [approve_selected, reject_selected]
    readonly_fields = ("created_at", "reviewed_at", "reviewed_by")
