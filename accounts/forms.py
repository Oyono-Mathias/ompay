from django import forms
from .models import KycRequest

class KycRequestForm(forms.ModelForm):
    class Meta:
        model = KycRequest
        fields = ["doc_type", "id_number", "date_of_birth", "address", "front_image", "back_image", "selfie_image"]
        widgets = {
            "doc_type": forms.Select(attrs={"class": "form-select"}),
            "id_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Numéro du document"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
