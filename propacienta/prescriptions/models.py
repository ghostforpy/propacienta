from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class BasePrescription(models.Model):
    """Абстрактная базовая модель назначения врача."""

    medicine_card = models.ForeignKey(
        "medicine_cards.medicinecard",
        on_delete=models.DO_NOTHING,
        related_name="%(class)s",
        verbose_name=_("Медицинская карта"),
    )
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Пациент"),
        related_name="%(class)s",
        null=True,
    )
    doctor = models.ForeignKey(
        "doctors.doctor",
        on_delete=models.DO_NOTHING,
        related_name="%(class)s",
        verbose_name=_("Врач"),
    )
    doctor_appointment = models.ForeignKey(
        "appointments.doctorappointment",
        on_delete=models.DO_NOTHING,
        related_name="%(class)s",
        verbose_name=_("Прием врача"),
    )

    class Meta:
        abstract = True


class Prescription(BasePrescription):
    """Абстрактная модель назначения врача."""

    duration = models.PositiveIntegerField(_("Продолжительность"))
    rate = models.PositiveIntegerField(_("Частота"))
    number = models.FloatField(_("Количество"))
    per = models.CharField(
        _("Единица измерения частоты"),
        help_text="День, неделя, месяц, час",
        max_length=20,
    )

    class Meta:
        abstract = True


class MedicinePrescription(Prescription):
    """Модель назначения медикаментов."""

    medicine = models.ForeignKey(
        "medicines.medicine",
        on_delete=models.DO_NOTHING,
        related_name="medicine_prescriptions",
        verbose_name=_("Медикамент"),
    )

    class Meta:
        verbose_name = "Назначение медикаментов"
        verbose_name_plural = "Назначения медикаментов"

    def __str__(self) -> str:
        return "{} для {}".format(self.Meta.verbose_name, self.medicine_card.pacient)


class ProcedurePrescription(Prescription):
    """Модель назначения процедур."""

    procedure = models.ForeignKey(
        "procedures.procedure",
        on_delete=models.DO_NOTHING,
        related_name="procedure_prescriptions",
        verbose_name=_("Процедура"),
    )

    class Meta:
        verbose_name = "Назначение процедуры"
        verbose_name_plural = "Назначения процедур"

    def __str__(self) -> str:
        return "{} для {}".format(self.Meta.verbose_name, self.medicine_card.pacient)


class AnalisisPrescription(BasePrescription):
    """Модель назначения анализа."""

    analisis = models.ForeignKey(
        "analisis.analysis",
        on_delete=models.DO_NOTHING,
        related_name="analisis_prescriptions",
        verbose_name=_("Анализ"),
    )

    class Meta:
        verbose_name = "Назначение анализа"
        verbose_name_plural = "Назначения анализов"

    def __str__(self) -> str:
        return "{} для {}".format(self.Meta.verbose_name, self.medicine_card.pacient)
