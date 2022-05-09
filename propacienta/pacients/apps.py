from django.apps import AppConfig
from django.conf import settings


class PacientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pacients"
    verbose_name = "Пациенты"

    def ready(self):
        if not settings.DEBUG:
            import pacients.auditlog
