from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import DO_NOTHING, CharField, DateField, EmailField, OneToOneField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, username=None, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().select_related("pacient", "doctor")


class User(AbstractUser):
    """
    Default custom user model for propacienta.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    email = EmailField(_("email address"), unique=True)
    username = CharField(blank=True, max_length=255)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("Имя"), blank=True, max_length=255)
    last_name = CharField(_("Фамилия"), blank=True, max_length=255)
    patronymic = CharField(_("Отчество"), blank=True, max_length=255)
    birthday = DateField(_("Дата рождения"), null=True)
    pacient = OneToOneField(
        "pacients.pacient", on_delete=DO_NOTHING, null=True, related_name="user"
    )
    doctor = OneToOneField(
        "doctors.doctor", on_delete=DO_NOTHING, null=True, related_name="user", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "patronymic"]

    objects = CustomUserManager()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"id": self.id})

    def get_api_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("api:users-detail", kwargs={"id": self.id})

    def get_fio(self):
        return '{} {}.{}.'.format(
            self.last_name,
            self.first_name[0].upper(),
            self.patronymic[0].upper()
        )
