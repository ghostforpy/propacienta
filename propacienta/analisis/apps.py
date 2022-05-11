from django.apps import AppConfig
from django.conf import settings


class AnalisisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "analisis"
    verbose_name = "Анализы"

    def ready(self):
        import analisis.signals

        if not settings.DEBUG:
            import analisis.auditlog
