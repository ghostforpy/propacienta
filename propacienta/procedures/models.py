from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Procedure(models.Model):
    """Procedure model."""

    title = models.CharField(_("Наименование"), max_length=250, unique=True)

    class Meta:
        verbose_name = "Процедура"
        verbose_name_plural = "Процедуры"

    def __str__(self) -> str:
        return self.title
