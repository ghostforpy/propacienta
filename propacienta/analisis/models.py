from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Analysis(models.Model):
    """Analysis model."""
    title = models.CharField(
        _("Наименование"),
        max_length=250,
        unique=True
        )
    
    class Meta:
        verbose_name = "Анализ"
        verbose_name_plural = "Анализы"

    def __str__(self) -> str:
        return self.title