from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Doctor(models.Model):
    """Model for doctors."""
    #user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
    phone = models.CharField(_("Телефон"), max_length=30)
    hospitals = models.ManyToManyField(
        "hospitals.hospital",
        verbose_name=_("Клиники"),
        related_name="doctors"
    )
    
    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self) -> str:
        return "{} {}".format(self.user.first_name, self.user.last_name)