from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_image_size(file):
    max_mb = 5
    if file.size > max_mb * 1024 * 1024:
        raise ValidationError(f"Image trop lourde (>{max_mb} MB).")

def kyc_upload_path(instance, filename):
    # media/kyc/<user_id>/<filename>
    return f"kyc/{instance.user_id}/{filename}"

class User(AbstractUser):
    phone_number = models.CharField("Téléphone", max_length=20, blank=True, null=True)
    country = models.CharField("Pays", max_length=60, blank=True, null=True)

    def __str__(self):
        return self.username


class KycRequest(models.Model):
    DOC_ID = "ID_CARD"
    DOC_PASSPORT = "PASSPORT"
    DOC_DRIVER = "DRIVER_LICENSE"
    DOC_TYPES = [
        (DOC_ID, "Carte d'identité"),
        (DOC_PASSPORT, "Passeport"),
        (DOC_DRIVER, "Permis de conduire"),
    ]

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    STATUSES = [
        (PENDING, "En attente"),
        (APPROVED, "Approuvé"),
        (REJECTED, "Refusé"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="kyc_requests")
    doc_type = models.CharField("Type de document", max_length=20, choices=DOC_TYPES)
    id_number = models.CharField("Numéro du document", max_length=64, blank=True)
    date_of_birth = models.DateField("Date de naissance", blank=True, null=True)
    address = models.TextField("Adresse", blank=True)

    front_image = models.ImageField("Document (recto)", upload_to=kyc_upload_path, validators=[validate_image_size])
    back_image = models.ImageField("Document (verso)", upload_to=kyc_upload_path, validators=[validate_image_size], blank=True, null=True)
    selfie_image = models.ImageField("Selfie avec document", upload_to=kyc_upload_path, validators=[validate_image_size])

    status = models.CharField(max_length=20, choices=STATUSES, default=PENDING)
    review_notes = models.TextField("Notes de revue (admin)", blank=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="kyc_reviews")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"KYC {self.user.username} [{self.get_status_display()}]"

    @property
    def is_final(self):
        return self.status in (self.APPROVED, self.REJECTED)
