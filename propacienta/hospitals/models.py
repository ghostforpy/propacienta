from pyexpat import model
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class HospitalTown(models.Model):
    title = models.CharField(_("Наименование"), unique=True, max_length=150)

    def __str__(self) -> str:
        return self.title


class Hospital(models.Model):
    title = models.CharField(_("Наименование"), unique=True, max_length=150)
    town = models.ForeignKey(
        HospitalTown,
        verbose_name=_("Населенный пункт"),
        on_delete=models.DO_NOTHING,
        related_name="hospitals"
    )
    address = models.CharField(_("Адрес"), max_length=250)

    def __str__(self) -> str:
        return self.title