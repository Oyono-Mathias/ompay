# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("kyc/", views.kyc_status, name="kyc_status"),
    path("kyc/submit/", views.kyc_submit, name="kyc_submit"),
]
