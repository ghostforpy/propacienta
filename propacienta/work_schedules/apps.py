from django.apps import AppConfig

# from django.conf import settings


class WorkSchedulesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "work_schedules"
    verbose_name = "Графики работы"

    # def ready(self):
    #     if not settings.DEBUG:
    #         import pacients.auditlog
