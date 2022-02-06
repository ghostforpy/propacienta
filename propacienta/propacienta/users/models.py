from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField, OneToOneField, DO_NOTHING

from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for propacienta.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First name"), blank=True, max_length=255)
    last_name = CharField(_("Last name"), blank=True, max_length=255)
    patronymic = CharField(_("Patronymic"), blank=True, max_length=255)
    birthday = DateField(null=True)
    pacient = OneToOneField("pacients.pacient", on_delete=DO_NOTHING, null=True, related_name="user")
    doctor = OneToOneField("doctors.doctor", on_delete=DO_NOTHING, null=True, related_name="user")

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
    

