from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Pacient(models.Model):
    """Model for pacients."""
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
    phone = models.CharField(_("Телефон"))
