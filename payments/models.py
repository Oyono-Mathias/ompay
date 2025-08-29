from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet({self.user.username})"


class Transaction(models.Model):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    TRANSFER_OUT = "TRANSFER_OUT"
    TRANSFER_IN = "TRANSFER_IN"

    TX_TYPES = [
        (DEPOSIT, "Dépôt"),
        (WITHDRAW, "Retrait"),
        (TRANSFER_OUT, "Transfert sortant"),
        (TRANSFER_IN, "Transfert entrant"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    tx_type = models.CharField(max_length=20, choices=TX_TYPES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    reference = models.CharField(max_length=64, blank=True)
    related_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_transactions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tx_type} {self.amount} pour {self.user.username}"
