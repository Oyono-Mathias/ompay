from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("deposit/", views.deposit_view, name="deposit"),
    path("withdraw/", views.withdraw_view, name="withdraw"),
    path("transfer/", views.transfer_view, name="transfer"),
]
