from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.

class DoctorSpecialization(models.Model):
    title = models.CharField(
        _("Специализация"),
        max_length=250,
        unique=True
        )
    
    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"

    def __str__(self) -> str:
        return self.title


class DoctorSubSpecialization(models.Model):
    title = models.CharField(
        _("Узкая специализация"),
        max_length=250,
        unique=True
        )
    specialization = models.ForeignKey(
        DoctorSpecialization,
        on_delete=models.CASCADE,
        related_name="sub_specializations"
        )
    
    class Meta:
        verbose_name = "Узкая специализация"
        verbose_name_plural = "Узкие специализации"

    def __str__(self) -> str:
        return self.title


class Doctor(models.Model):
    """Model for doctors."""
    #user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
    phone = models.CharField(_("Телефон"), max_length=30)
    hospitals = models.ManyToManyField(
        "hospitals.hospital",
        verbose_name=_("Клиники"),
        related_name="doctors"
    )
    specializations = models.ManyToManyField(
        DoctorSpecialization,
        related_name="doctors"
    )
    sub_specializations = models.ManyToManyField(
        DoctorSubSpecialization,
        related_name="doctors"
    )

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self) -> str:
        return "{} {}".format(self.user.first_name, self.user.last_name)