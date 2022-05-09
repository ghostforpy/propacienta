from django.apps import AppConfig


class DiseasesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "diseases"
    verbose_name = "Диагнозы и заболевания"

    def ready(self):
        import diseases.signals
