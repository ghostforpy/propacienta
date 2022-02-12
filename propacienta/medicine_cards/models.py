from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class MedicineCard(models.Model):
    pacient = models.OneToOneField(
        "pacients.pacient",
        on_delete=models.CASCADE,
        related_name="medicine_card",
        verbose_name=_("Пациент")
    )
    height = models.DecimalField(_("Рост"), max_digits=8, decimal_places=2, null=True)
    weight = models.DecimalField(_("Вес"), max_digits=8, decimal_places=2, null=True)
    average_pressure = models.CharField(max_length=20, null=True, verbose_name=_("Среднее давление"))

    class Meta:
        verbose_name = "Медицинская карта"
        verbose_name_plural = "Медицинские карты"

    def __str__(self) -> str:
        return "Медицинская карта {}".format(self.pacient)


class IndependentResearch(models.Model):
    """Модель самостоятельных исследований (уровень сахара, давление и т.д.)."""
    title = models.CharField(
        _("Наименование"),
        max_length=250,
        unique=True
        )

    class Meta:
        verbose_name = "Самостоятельное исследование"
        verbose_name_plural = "Самостоятельные исследования"

    def __str__(self) -> str:
        return self.title


class ResultIndependentResearch(models.Model):
    independent_research = models.ForeignKey(
        IndependentResearch,
        on_delete=models.DO_NOTHING,
        verbose_name=(_("Самостоятельное исследование")),
        related_name="independent_research_results"
    )
    medicine_card = models.ForeignKey(
        MedicineCard,
        on_delete=models.DO_NOTHING,
        related_name="independent_research_results"
    )
    result = models.TextField(_("Результат"))

    class Meta:
        verbose_name = "Результат самостоятельного исследования"
        verbose_name_plural = "Результаты самостоятельных исследований"

    def __str__(self) -> str:
        return self.title