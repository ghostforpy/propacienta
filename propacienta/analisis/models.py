import imp
from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import analisis_result_dir
# Create your models here.

class Analysis(models.Model):
    """Analysis model."""
    title = models.CharField(
        _("Наименование"),
        max_length=250,
        unique=True
        )
    
    class Meta:
        verbose_name = "Анализ"
        verbose_name_plural = "Анализы"

    def __str__(self) -> str:
        return self.title


class AnalysisResult(models.Model):
    """Модель результата анализа."""
    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Анализ"),
        related_name="analysi_results"
    )
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Пациент"),
        related_name="analysi_results"
    )
    medicine_card = models.ForeignKey(
        "medicine_cards.medicinecard",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Медицинская карта"),
        related_name="analysi_results"
    )
    prescription = models.ForeignKey(
        "prescriptions.analisisprescription",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Назначение"),
        related_name="analysi_results"
    )
    result = models.TextField(_("Результаты анализа"))
    d = models.DateField(_("Дата сдачи анализа"))
    
    class Meta:
        verbose_name = "Результат анализа"
        verbose_name_plural = "Результаты анализов"

    def __str__(self) -> str:
        return "{} {}".format(self.analysis, self.pacient)


class AnalysisResultsImage(models.Model):
    analysis_result = models.ForeignKey(
        AnalysisResult,
        on_delete=models.DO_NOTHING,
        related_name="analysis_images"
    )
    image = models.ImageField(
        _("Фото"),
        upload_to=analisis_result_dir,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Изображение результата анализа"
        verbose_name_plural = "Изображения результатов анализов"

    def __str__(self) -> str:
        return "Изображение к {}".format(self.analysis_result)


class AnalysisResultsFile(models.Model):
    analysis_result = models.ForeignKey(
        AnalysisResult,
        on_delete=models.DO_NOTHING,
        related_name="analysis_files"
    )
    file = models.FileField(
        _("Файл"),
        upload_to=analisis_result_dir,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Файл результата анализа"
        verbose_name_plural = "Файлы результатов анализов"

    def __str__(self) -> str:
        return "Файл к {}".format(self.analysis_result)