from django.apps import AppConfig

class PaymentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payments"
    verbose_name = "Payments"

    def ready(self):
        # On branche les signaux ici (ne pas importer les modèles au niveau module)
        from . import signals  # noqa: F401
