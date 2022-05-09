from django.apps import AppConfig
from django.conf import settings


class MedicineCardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "medicine_cards"
    verbose_name = "Медицинские карты"

    def ready(self):
        if not settings.DEBUG:
            import medicine_cards.auditlog
