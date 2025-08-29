from django.contrib import admin
from .models import Wallet, Transaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "updated_at")
    search_fields = ("user__username", "user__email")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "tx_type", "amount", "reference", "related_user", "created_at")
    list_filter = ("tx_type", "created_at")
    search_fields = ("user__username", "reference")
