from django.apps import AppConfig
from django.conf import settings


class OperationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "operations"
    verbose_name = "Операции"

    def ready(self):
        import operations.signals

        if not settings.DEBUG:
            import operations.auditlog
