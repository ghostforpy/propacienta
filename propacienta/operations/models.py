from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from .utils import transferred_operation_files_dir, transferred_operation_images_dir


# Create your models here.
class Operation(models.Model):
    """Модель операции."""

    title = models.CharField(_("Наименование"), max_length=250, unique=True)

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.title


class TransferredOperation(models.Model):
    """Модель перенесенной операции."""

    operation = models.ForeignKey(
        Operation,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Операция"),
        related_name="transferred_operations",
    )
    medicine_card = models.ForeignKey(
        "medicine_cards.medicinecard",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Медицинская карта"),
        related_name="transferred_operations",
    )
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Пациент"),
        related_name="transferred_operations",
    )
    effect = models.CharField(_("Эффект"), max_length=250, default="", blank=True)
    place = models.CharField(
        _("Место проведения операции"), max_length=250, default="", blank=True
    )
    date = models.DateField(_("Дата проведения операции"), null=True)

    class Meta:
        verbose_name = "Перенесенная операция"
        verbose_name_plural = "Перенесенные операции"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "{} {}".format(self.pacient, self.operation)


class TransferredOperationImage(models.Model):
    """Модель изображения выписного эпикриза перенесенной операции."""

    transferred_operation = models.ForeignKey(
        TransferredOperation,
        on_delete=models.CASCADE,
        related_name="transferred_operation_images",
    )
    image = models.ImageField(
        _("Фото"), upload_to=transferred_operation_images_dir, null=True, blank=True
    )

    class Meta:
        verbose_name = "Изображение выписного эпикриза перенесенной операции"
        verbose_name_plural = "Изображения выписных эпикризов перенесенных операций"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "Изображение к {}".format(self.transferred_operation)

    def get_absolute_url(self):
        return reverse(
            "api:transferred-operation-images-delete", kwargs={"pk": self.pk}
        )

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class TransferredOperationFile(models.Model):
    """Модель файла выпиского эпикриза перенесенной операции."""

    transferred_operation = models.ForeignKey(
        TransferredOperation,
        on_delete=models.CASCADE,
        related_name="transferred_operation_files",
    )
    file = models.FileField(
        _("Файл"), upload_to=transferred_operation_files_dir, null=True, blank=True
    )

    class Meta:
        verbose_name = "Файл выписного эпикриза перенесенной операции"
        verbose_name_plural = "Файлы выписных эпикризов перенесенных операций"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "Файл к {}".format(self.transferred_operation)

    def get_absolute_url(self):
        return reverse("api:transferred-operation-files-delete", kwargs={"pk": self.pk})

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
