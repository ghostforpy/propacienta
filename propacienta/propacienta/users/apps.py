from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "propacienta.users"
    verbose_name = _("Пользователи")

    def ready(self):
        try:
            import propacienta.users.signals  # noqa F401
        except ImportError:
            pass
