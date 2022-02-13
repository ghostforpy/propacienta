from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Operation(models.Model):
    """Модель операции."""
    title = models.CharField(
        _("Наименование"),
        max_length=250,
        unique=True
        )

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"

    def __str__(self) -> str:
        return self.title


class TransferredOperation(models.Model):
    """Модель перенесенной операции."""
    operation = models.ForeignKey(
        Operation,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Операция"),
        related_name="transferred_operations"
    )
    medicine_card = models.ForeignKey(
        "medicine_cards.medicinecard",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Медицинская карта"),
        related_name="transferred_operations"
    )
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Пациент"),
        related_name="transferred_operations"
    )
    effect = models.CharField(_("Эффект"), max_length=250)
    date = models.DateField(_("Дата проведения операции"), null=True)

    class Meta:
        verbose_name = "Перенесенная операция"
        verbose_name_plural = "Перенесенные операции"

    def __str__(self) -> str:
        return "{} {}".format(self.pacient, self.operation)