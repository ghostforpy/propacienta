from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class HospitalTown(models.Model):
    """Town where hospital is located."""

    title = models.CharField(_("Наименование"), unique=True, max_length=150)

    class Meta:
        verbose_name = "Населенный пункт"
        verbose_name_plural = "Населенные пункты"

    def __str__(self) -> str:
        return self.title


class Hospital(models.Model):
    """Hospital model."""

    title = models.CharField(_("Наименование"), unique=True, max_length=150)
    town = models.ForeignKey(
        HospitalTown,
        verbose_name=_("Населенный пункт"),
        on_delete=models.DO_NOTHING,
        related_name="hospitals",
    )
    address = models.CharField(_("Адрес"), max_length=250)

    class Meta:
        verbose_name = "Клиника"
        verbose_name_plural = "Клиники"

    def __str__(self) -> str:
        return self.title


DEFAULT_HOSPITAL = Hospital.objects.first()
