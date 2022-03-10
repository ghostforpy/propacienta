from traceback import print_tb
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.signals import user_registered
# Create your models here.


class Pacient(models.Model):
    """Model for pacients."""
    phone = models.CharField(_("Телефон"), max_length=30, unique=True)
    
    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self) -> str:
        try:
            return "{} {}".format(self.user.first_name, self.user.last_name)
        except Pacient.user.RelatedObjectDoesNotExist:
            return super().__str__()

def user_created(signal=None, sender=None, user=None, request=None, **kwargs):
    phone_pacient = request.data['phone_pacient']
    pacient = Pacient.objects.create(phone=phone_pacient)
    user.pacient = pacient
    user.save()

user_registered.connect(user_created)