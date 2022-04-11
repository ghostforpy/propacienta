from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from .utils import discharge_epicrisis_files_dir, discharge_epicrisis_images_dir


class Disease(models.Model):
    """Модель заболевания."""
    title = models.CharField(
        _("Наименование"),
        max_length=250,
        unique=True
        )
    code = models.CharField(_("Код"), max_length=50, unique=True)

    class Meta:
        verbose_name = "Болезнь"
        verbose_name_plural = "Болезни"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "{} код {}".format(self.title, self.code)


class ChronicDisease(models.Model):
    """Модель хронических заболеваний."""
    disease = models.ForeignKey(
        Disease,
        on_delete=models.CASCADE,
        verbose_name=_("Заболенивание"),
        related_name="chronic_diseases"
    )
    medicine_card = models.ForeignKey(
        "medicine_cards.medicinecard",
        on_delete=models.CASCADE,
        verbose_name=_("Медицинская карта"),
        related_name="chronic_diseases"
    )
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.CASCADE,
        verbose_name=_("Пациент"),
        related_name="chronic_diseases"
    )
    treatment = models.TextField(_("Лечение"), null=True, blank=True)

    class Meta:
        verbose_name = "Хроническое заболевание"
        verbose_name_plural = "Хронические заболевания"
        ordering = ["-id"]
        unique_together = ['disease', 'pacient']

    def __str__(self) -> str:
        return "{} {}".format(self.pacient, self.disease)


class DischargeEpicris(models.Model):
    """Модель выписного эпикриза для хронических заболеваний."""
    chronic_disease = models.ForeignKey(
        ChronicDisease,
        on_delete=models.CASCADE,
        verbose_name=_("Хроничекое заболенивание"),
        related_name="discharge_epicrisis"
    )
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.CASCADE,
        verbose_name=_("Пациент"),
        related_name="discharge_epicrisis"
    )
    d = models.DateField(_("Дата"))
    epicris = models.TextField(_("Эпикриз"), null=True, blank=True)

    class Meta:
        verbose_name = "Выписной эпикриз"
        verbose_name_plural = "Выписные эпикризы"
        ordering = ["-d", "-id"]

    def __str__(self) -> str:
        return "Выписной эпикриз {} {} {}".format(
            self.pacient,
            self.chronic_disease.disease,
            self.d
        )

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if DischargeEpicris.objects.filter(
            chronic_disease=self.chronic_disease,
            pacient=self.pacient
        ).count() <= 0:
            self.chronic_disease.delete()


class DischargeEpicrisImage(models.Model):
    """Модель изображения выпиского эпикриза."""
    discharge_epicris = models.ForeignKey(
        DischargeEpicris,
        on_delete=models.CASCADE,
        related_name="discharge_epicrisis_images"
    )
    image = models.ImageField(
        _("Фото"),
        upload_to=discharge_epicrisis_images_dir,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Изображение выписного эпикриза"
        verbose_name_plural = "Изображения выписных эпикризов"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "Изображение к {}".format(self.discharge_epicris)

    def get_absolute_url(self):
        return reverse("api:discharge-epicris-images-delete", kwargs={"pk": self.pk})

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class DischargeEpicrisFiles(models.Model):
    """Модель файла выпиского эпикриза."""
    discharge_epicris = models.ForeignKey(
        DischargeEpicris,
        on_delete=models.CASCADE,
        related_name="discharge_epicrisis_files"
    )
    file = models.FileField(
        _("Файл"),
        upload_to=discharge_epicrisis_files_dir,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Файл выписного эпикриза"
        verbose_name_plural = "Файлы выписных эпикризов"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "Файл к {}".format(self.discharge_epicris)

    def get_absolute_url(self):
        return reverse("api:discharge-epicris-files-delete", kwargs={"pk": self.pk})

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class TransferredDisease(models.Model):
    """Модель перенесенного заболевания."""
    disease = models.ForeignKey(
        Disease,
        on_delete=models.CASCADE,
        verbose_name=_("Заболевание"),
        related_name="transferred_diseases"
    )
    medicine_card = models.ForeignKey(
        "medicine_cards.medicinecard",
        on_delete=models.CASCADE,
        verbose_name=_("Медицинская карта"),
        related_name="transferred_diseases"
    )
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.CASCADE,
        verbose_name=_("Пациент"),
        related_name="transferred_diseases"
    )
    diagnosis = models.CharField(_("Диагноз"), max_length=250)
    diagnosis_date = models.DateField(_("Дата постановки диагноза"), null=True)
    diagnosis_year = models.PositiveIntegerField(_("Год постановки диагноза"), null=True)
    treatment_date = models.DateField(_("Дата начала лечения"), null=True)
    treatment_end_date = models.DateField(_("Дата окончания лечения"), null=True)

    class Meta:
        verbose_name = "Перенесенное заболевание"
        verbose_name_plural = "Перенесенные заболевания"
        ordering = ["-treatment_end_date", "-treatment_date", "-id"]

    def __str__(self) -> str:
        return "{} {}".format(self.pacient, self.disease)
