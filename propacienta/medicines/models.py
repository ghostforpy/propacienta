from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Medicine(models.Model):
    """Medicine model."""

    title = models.CharField(_("Наименование"), max_length=250, unique=True)

    class Meta:
        verbose_name = "Медикамент"
        verbose_name_plural = "Медикаменты"

    def __str__(self) -> str:
        return self.title
