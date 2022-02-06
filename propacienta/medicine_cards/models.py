from statistics import mode
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class MedicineCard(models.Model):
    pacient = models.OneToOneField(
        "pacients.pacient",
        on_delete=models.CASCADE,
        related_name="medicine_card",
        verbose_name=_("Medicine card")
    )
    height = models.DecimalField(_("Height"), max_digits=8, decimal_places=2, null=True)
    weight = models.DecimalField(_("Weight"), max_digits=8, decimal_places=2, null=True)
    average_pressure = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = "Медицинская карта"
        verbose_name_plural = "Медицинские карты"