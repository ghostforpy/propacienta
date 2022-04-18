from django.apps import AppConfig


class RequestsLogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "requests_logs"
    verbose_name = "Запросы в БД"
