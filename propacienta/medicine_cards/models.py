from django.db import models
from django.utils.translation import gettext_lazy as _

from pacients.signals import pacient_created

# Create your models here.


class MedicineCard(models.Model):
    GENDER_CHOISES = [
        ("male", "Мужской"),
        ("female", "Женский"),
    ]
    BLOOD_TYPE_CHOISES = [
        ("I−", "O(I) Rh−"),
        ("I+", "O(I) Rh+"),
        ("II−", "A(II) Rh−"),
        ("II+", "A(II) Rh+"),
        ("III−", "B(III) Rh−"),
        ("III+", "B(III) Rh+"),
        ("IV−", "AB(IV) Rh−"),
        ("IV+", "AB(IV) Rh+"),
    ]
    pacient = models.OneToOneField(
        "pacients.pacient",
        on_delete=models.CASCADE,
        related_name="medicine_card",
        verbose_name=_("Пациент"),
    )
    height = models.DecimalField(_("Рост"), max_digits=8, decimal_places=2, null=True)
    weight = models.DecimalField(_("Вес"), max_digits=8, decimal_places=2, null=True)
    average_pressure = models.CharField(
        max_length=20, null=True, verbose_name=_("Среднее давление")
    )
    gender = models.CharField(
        _("Пол"),
        max_length=6,
        default="male",
        choices=GENDER_CHOISES
    )
    blood_type = models.CharField(
        _("Группа крови"),
        max_length=6,
        default="I−",
        choices=BLOOD_TYPE_CHOISES
    )

    class Meta:
        verbose_name = "Медицинская карта"
        verbose_name_plural = "Медицинские карты"

    def __str__(self) -> str:
        return "Медицинская карта {}".format(self.pacient)


class IndependentResearch(models.Model):
    """Модель самостоятельных исследований (уровень сахара, давление и т.д.)."""

    title = models.CharField(_("Наименование"), max_length=250, unique=True)

    class Meta:
        verbose_name = "Самостоятельное исследование"
        verbose_name_plural = "Самостоятельные исследования"

    def __str__(self) -> str:
        return self.title


class ResultIndependentResearch(models.Model):
    independent_research = models.ForeignKey(
        IndependentResearch,
        on_delete=models.CASCADE,
        verbose_name=(_("Самостоятельное исследование")),
        related_name="independent_research_results",
    )
    medicine_card = models.ForeignKey(
        MedicineCard,
        on_delete=models.CASCADE,
        related_name="independent_research_results",
    )
    result = models.TextField(_("Результат"))
    datetime_stamp = models.DateTimeField(_("Время проведения"), blank=True, null=True)

    class Meta:
        verbose_name = "Результат самостоятельного исследования"
        verbose_name_plural = "Результаты самостоятельных исследований"
        ordering = ["-datetime_stamp", "-id"]

    def __str__(self) -> str:
        return self.independent_research.title


def create_medicine_card(signal=None, sender=None, pacient=None, **kwargs):
    medicine_card = MedicineCard.objects.create(pacient=pacient)
    medicine_card.save()


pacient_created.connect(create_medicine_card)
