from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import discharge_epicrisis_dir
# Create your models here.

class Disease(models.Model):
    """Модель заболевания."""
    title = models.CharField(
        _("Наименование"),
        max_length=250,
        unique=True
        )
    code = models.CharField(_("Код"), max_length=50)

    class Meta:
        verbose_name = "Болезнь"
        verbose_name_plural = "Болезни"

    def __str__(self) -> str:
        return "{} код {}".format(self.title, self.code)


class ChronicDisease(models.Model):
    """Модель хронических заболеваний."""
    disease = models.ForeignKey(
        Disease,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Заболенивание"),
        related_name="chronic_diseases"
    )
    medicine_card = models.ForeignKey(
        "medicine_cards.medicinecard",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Медицинская карта"),
        related_name="chronic_diseases"
    )
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Пациент"),
        related_name="chronic_diseases"
    )
    treatment = models.TextField(_("Лечение"))

    class Meta:
        verbose_name = "Хроническое заболевание"
        verbose_name_plural = "Хронические заболевания"

    def __str__(self) -> str:
        return "{} {}".format(self.pacient, self.disease)

class DischargeEpicris(models.Model):
    """Модель выписного эпикриза для хронических заболеваний."""
    chronic_disease = models.ForeignKey(
        ChronicDisease,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Хроничекое заболенивание"),
        related_name="discharge_epicrisis"
    )
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Пациент"),
        related_name="discharge_epicrisis"
    )
    d = models.DateField(_("Дата"))

    class Meta:
        verbose_name = "Выписной эпикриз"
        verbose_name_plural = "Выписные эпикризы"

    def __str__(self) -> str:
        return "Выписной эпикриз {} {} {}".format(
            self.pacient,
            self.chronic_disease.disease,
            self.d
        )


class DischargeEpicrisImage(models.Model):
    """Модель картинки выпиского эпикриза."""
    discharge_epicris = models.ForeignKey(
        DischargeEpicris,
        on_delete=models.DO_NOTHING,
        related_name="discharge_epicrisis_images"
    )
    image = models.ImageField(
        _("Фото"),
        upload_to=discharge_epicrisis_dir,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Изображение выписного эпикриза"
        verbose_name_plural = "Изображения выписных эпикризов"

    def __str__(self) -> str:
        return "Изображение к {}".format(self.discharge_epicris)


class DischargeEpicrisFiles(models.Model):
    """Модель файла  выпиского эпикриза."""
    discharge_epicris = models.ForeignKey(
        DischargeEpicris,
        on_delete=models.DO_NOTHING,
        related_name="discharge_epicrisis_files"
    )
    file = models.FileField(
        _("Файл"),
        upload_to=discharge_epicrisis_dir,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Файл выписного эпикриза"
        verbose_name_plural = "Файлы выписных эпикризов"

    def __str__(self) -> str:
        return "Файл к {}".format(self.discharge_epicris)