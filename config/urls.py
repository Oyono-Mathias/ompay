# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("payments/", include("payments.urls")),
    path("accounts/", include("accounts.urls")),  # ← IMPORTANT
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
