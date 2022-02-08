from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class AppointmentOrder(models.Model):
    """AppointmentOrder model."""
    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.DO_NOTHING,
        related_name="appointment_orders"
    )
    doctor = models.ForeignKey(
        "doctors.doctor",
        on_delete=models.DO_NOTHING,
        related_name="appointment_orders"
    )
    dt = models.DateTimeField(_("Время приема"), blank=True, null=True)
    confirmation = models.BooleanField(
        _("Подтверждение приема"),
        default=False
    )
    created_at = models.DateTimeField(
        _("Создан"),
        auto_now_add=True
    )
    appointment_took_place = models.BooleanField(_("Приём состоялся"), default=False)
    doctor_specialization = models.ForeignKey(
        "doctors.doctorspecialization",
        on_delete=models.DO_NOTHING,
        related_name="appointment_orders",
        null=True,
        blank=True
    )
    doctor_sub_specialization = models.ForeignKey(
        "doctors.doctorsubspecialization",
        on_delete=models.DO_NOTHING,
        related_name="appointment_orders",
        null=True,
        blank=True
    )
    hospital = models.ForeignKey(
        "hospitals.hospital",
        on_delete=models.DO_NOTHING,
        related_name="appointment_orders"
    )

    class Meta:
        verbose_name = "Заказ на приём врача"
        verbose_name_plural = "Заказы на приём врача"

    def __str__(self) -> str:
        return "{} к {}".format(self.pacient, self.doctor)