from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Pacient(models.Model):
    """Model for pacients."""
    phone = models.CharField(_("Телефон"), max_length=30)
    
    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self) -> str:
        return "{} {}".format(self.user.first_name, self.user.last_name)

