from decimal import Decimal
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        label="Montant à déposer",
        max_digits=14,
        decimal_places=2,
        min_value=Decimal("0.01"),
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ex: 1000.00"})
    )

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        label="Montant à retirer",
        max_digits=14,
        decimal_places=2,
        min_value=Decimal("0.01"),
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ex: 500.00"})
    )

class TransferForm(forms.Form):
    recipient_username = forms.CharField(
        label="Nom d’utilisateur du destinataire",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: jean"})
    )
    amount = forms.DecimalField(
        label="Montant à transférer",
        max_digits=14,
        decimal_places=2,
        min_value=Decimal("0.01"),
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ex: 2000.00"})
    )

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("recipient_username")
        if username:
            try:
                cleaned["recipient"] = User.objects.get(username=username)
            except User.DoesNotExist:
                self.add_error("recipient_username", "Utilisateur introuvable.")
        return cleaned
