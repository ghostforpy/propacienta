import pytz
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from hospitals.models import DEFAULT_HOSPITAL
from work_schedules.models import WorkDay


# Create your models here.
def default_hospital():
    return DEFAULT_HOSPITAL


class AppointmentOrder(models.Model):
    """AppointmentOrder model."""

    pacient = models.ForeignKey(
        "pacients.pacient",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Пациент"),
        related_name="appointment_orders",
    )
    doctor = models.ForeignKey(
        "doctors.doctor",
        verbose_name=_("Врач"),
        on_delete=models.DO_NOTHING,
        related_name="appointment_orders",
    )
    workday = models.ForeignKey(
        WorkDay,
        verbose_name=_("Рабочий период"),
        on_delete=models.DO_NOTHING,
        related_name="appointment_orders",
        null=True,
        blank=True,
    )
    dt = models.DateTimeField(_("Время приема"), blank=True, null=True)
    end = models.DateTimeField(_("Окончание приема"), blank=True, null=True)
    confirmation = models.BooleanField(_("Подтверждение приема"), default=False)
    created_at = models.DateTimeField(_("Создан"), auto_now_add=True)
    appointment_took_place = models.BooleanField(_("Приём состоялся"), default=False)
    doctor_specialization = models.ForeignKey(
        "doctors.doctorspecialization",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Специализация врача"),
        related_name="appointment_orders",
        null=True,
        blank=True,
    )
    doctor_sub_specialization = models.ForeignKey(
        "doctors.doctorsubspecialization",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Узкая специализация врача"),
        related_name="appointment_orders",
        null=True,
        blank=True,
    )
    hospital = models.ForeignKey(
        "hospitals.hospital",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Клиника"),
        related_name="appointment_orders",
        default=default_hospital
    )

    class Meta:
        verbose_name = "Заказ на приём врача"
        verbose_name_plural = "Заказы на приём врача"

    def __str__(self) -> str:
        return "{} к {}".format(self.pacient, self.doctor)

    def get_pacient_name(self):
        return "{} {}.{}.".format(
            self.pacient.user.last_name,
            self.pacient.user.first_name[0].upper(),
            self.pacient.user.patronymic[0].upper(),
        )

    def get_doctor_name(self):
        return "{} {}.{}.".format(
            self.doctor.user.last_name,
            self.doctor.user.first_name[0].upper(),
            self.doctor.user.patronymic[0].upper(),
        )

    def delete(self):
        dt = self.dt.astimezone(tz=pytz.timezone(settings.TIME_ZONE))
        w = WorkDay.objects.filter(
                doctor=self.doctor,
                date=dt.date(),
                since__lte=dt.time(),
                to__gt=dt.time(),
            ).get()
        w.cancel_reserve_timeslot(dt.time())
        return super().delete()


class AppointmentSurvey(models.Model):
    """Модель опросника для пациента перед приемом у врача."""

    appointment_order = models.OneToOneField(
        AppointmentOrder,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Заказ на приём врача"),
        related_name="survey",
    )
    complaints = models.TextField(_("Жалобы"), blank=True, default="")
    complaints_date = models.DateField(_("Когда впервые появились жалобы"), blank=True)
    treatment = models.TextField(_("Лечение"), blank=True, default="")

    class Meta:
        verbose_name = "Опросник перед приёмом врача"
        verbose_name_plural = "Опросники перед приёмом врача"

    def __str__(self) -> str:
        return "{} к {}".format(self.pacient, self.doctor)


class DoctorAppointment(models.Model):
    """Модель факта проведения приема у врача."""

    pacient = models.ForeignKey(
        "pacients.pacient",
        verbose_name=_("Пациент"),
        on_delete=models.DO_NOTHING,
        related_name="doctor_appointments",
    )
    doctor = models.ForeignKey(
        "doctors.doctor",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Врач"),
        related_name="doctor_appointments",
    )
    dt = models.DateTimeField(_("Фактическое время приема"))
    appointment_order = models.OneToOneField(
        AppointmentOrder,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Заказ на приём врача"),
        related_name="doctor_appointment",
        blank=True,
        null=True,
    )
    anamnesis = models.TextField(_("Анамнез"), blank=True, default="")
    medicine_card = models.ForeignKey(
        "medicine_cards.medicinecard",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Медицинская карта"),
        related_name="doctor_appointments",
    )
    doctor_specialization = models.ForeignKey(
        "doctors.doctorspecialization",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Специализация врача"),
        related_name="doctor_appointments",
        null=True,
        blank=True,
    )
    doctor_sub_specialization = models.ForeignKey(
        "doctors.doctorsubspecialization",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Узкая специализация врача"),
        related_name="doctor_appointments",
        null=True,
        blank=True,
    )
    hospital = models.ForeignKey(
        "hospitals.hospital",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Клиника"),
        related_name="doctor_appointments",
        null=True,
    )
    complaints = models.TextField(_("Жалобы"), default="", blank=True)
    complaints_date = models.DateField(_("Когда впервые появились жалобы"), blank=True)
    treatment = models.TextField(_("Лечение"), default="", blank=True)
    rating_for_pacient = models.FloatField(_("Оценка пациенту"), blank=True, null=True)
    rating_for_doctor = models.FloatField(_("Оценка доктору"), blank=True, null=True)

    class Meta:
        verbose_name = "Приём врача"
        verbose_name_plural = "Приёмы врачей"

    def __str__(self) -> str:
        return "{} к {}".format(self.pacient, self.doctor)
