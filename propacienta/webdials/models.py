from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class WebDial(models.Model):
    """Users webdial model."""
    END_WEBDIAL_REASONS = [
        ("initiator", _("Инициатор")),
        ("opponent", _("Вызываемый")),
        ("error", _("Ошибка")),
        ("opponent_reject", _("Отбой")),
    ]
    uuid = models.UUIDField("Идентификатор")
    initiator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Инициатор"),
        related_name="initiator_webdials"
    )
    opponent = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Вызываемый пользователь"),
        related_name="opponent_webdials"
    )
    start_webdial = models.DateTimeField(_("Начало разговора"), auto_now_add=True)
    end_webdial = models.DateTimeField(_("Окончание разговора"), blank=True, null=True)
    webdial_duration = models.DurationField(
        _("Продолжительность разговора"),
        blank=True,
        null=True
    )
    end_webdial_reason = models.CharField(
        _("Причина окончания разговора"),
        blank=True,
        choices=END_WEBDIAL_REASONS,
        default="error",
        max_length=20
        )
    webdial_happen = models.BooleanField(
        _("Звонок состоялся"),
        default=False
    )

    class Meta:
        verbose_name = "Звонок"
        verbose_name_plural = "Звонки"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "Звонок между {} и {}".format(self.initiator.get_fio(), self.opponent.get_fio())
