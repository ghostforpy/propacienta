from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Dialog(models.Model):
    """Users dialog model."""
    members = models.ManyToManyField(
        get_user_model(),
        "dialogs"
    )

    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "Диалог между {} и {}".format(*self.members.all())


class DialogMessage(models.Model):
    """Dialog message model."""
    dialog = models.ForeignKey(
        Dialog,
        on_delete=models.CASCADE,
        verbose_name="Диалог",
        related_name="messages"
    )
    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Автор сообщения",
        related_name="dialog_messages"
    )
    message = models.CharField(
        "Текст сообщения",
        max_length=1000
    )
    created_at = models.DateTimeField(_("Создан"), auto_now_add=True)
    received_by_the_server = models.BooleanField(_("Получено сервером"), default=True)
    sent_by_the_server = models.BooleanField(_("Отправлено сервером"), default=False)
    received_by_the_user = models.BooleanField(_("Получено пользователем"), default=False)
    read_by_the_user = models.BooleanField(_("Прочитано пользователем"), default=False)

    class Meta:
        verbose_name = "Сообщение диалога"
        verbose_name_plural = "Сообщения диалогов"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "Сообщение диалога между {} и {}".format(*self.dialog.members.all())
