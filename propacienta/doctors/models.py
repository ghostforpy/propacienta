from django.db import models
from django.utils.translation import gettext_lazy as _
from djoser.signals import user_registered

from .utils import doctor_avatar_dir


class DoctorSpecialization(models.Model):
    title = models.CharField(_("Наименование"), max_length=250, unique=True)

    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"

    def __str__(self) -> str:
        return self.title


class DoctorSubSpecialization(models.Model):
    title = models.CharField(_("Наименование"), max_length=250, unique=True)
    specialization = models.ForeignKey(
        DoctorSpecialization,
        on_delete=models.CASCADE,
        verbose_name=_("Специализация"),
        related_name="sub_specializations",
    )

    class Meta:
        verbose_name = "Узкая специализация"
        verbose_name_plural = "Узкие специализации"

    def __str__(self) -> str:
        return self.title


class Doctor(models.Model):
    """Model for doctors."""

    # user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
    phone = models.CharField(_("Телефон"), max_length=30, unique=True)
    hospitals = models.ManyToManyField(
        "hospitals.hospital",
        verbose_name=_("Клиники"),
        related_name="doctors",
        blank=True,
    )
    specializations = models.ManyToManyField(
        DoctorSpecialization,
        verbose_name=_("Специализации"),
        related_name="doctors",
        blank=True,
    )
    sub_specializations = models.ManyToManyField(
        DoctorSubSpecialization,
        verbose_name=_("Узкие специализации"),
        related_name="doctors",
        blank=True,
    )
    is_active = models.BooleanField(_("Активация"), default=False)
    avatar = models.ImageField(
        _("Аватар"), upload_to=doctor_avatar_dir, null=True, blank=True
    )
    portfolio = models.TextField(_("Портфолио"), null=True, blank=True)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ["-id"]

    def __str__(self) -> str:
        try:
            return "{} {}".format(self.user.first_name, self.user.last_name)
        except Doctor.user.RelatedObjectDoesNotExist:
            return super().__str__()


def user_created(signal=None, sender=None, user=None, request=None, **kwargs):
    role_doctor = request.data["role_doctor"]
    phone_doctor = request.data["phone_doctor"]
    if role_doctor:
        doctor = Doctor.objects.create(phone=phone_doctor)
        user.doctor = doctor
        user.save()


user_registered.connect(user_created)
