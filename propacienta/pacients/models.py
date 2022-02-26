from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.signals import user_registered
# Create your models here.


class Pacient(models.Model):
    """Model for pacients."""
    phone = models.CharField(_("Телефон"), max_length=30)
    
    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self) -> str:
        return "{} {}".format(self.user.first_name, self.user.last_name)

def user_created(signal=None, sender=None, user=None, request=None, **kwargs):
    pacient = Pacient.objects.create()
    user.pacient = pacient
    user.save()

user_registered.connect(user_created)