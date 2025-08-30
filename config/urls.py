from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import home
from django.conf import settings
from django.conf.urls.static import static

# ← PATCH: on importe les vues KYC directement
from accounts.views import kyc_status, kyc_submit

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("payments/", include("payments.urls")),

    # ← PATCH: routes directes (bypass de include) pour garantir que ça marche
    path("accounts/kyc/", kyc_status, name="accounts-kyc-direct"),
    path("accounts/kyc/submit/", kyc_submit, name="accounts-kyc-submit-direct"),

    # on garde quand même l'include normal
    path("accounts/", include("accounts.urls")),
]

# Servir les fichiers MEDIA (images KYC)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
