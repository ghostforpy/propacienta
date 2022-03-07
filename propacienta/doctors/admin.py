from django.contrib import admin
from .models import Doctor, DoctorSpecialization, DoctorSubSpecialization
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from hospitals.models import Hospital


class UserModelAdmin(admin.StackedInline):
    model = get_user_model()
    fields = [
        "first_name",
        "last_name",
        "patronymic",
        "birthday"
    ]

# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("email", "user_name", "phone", "is_active")
    inlines = [UserModelAdmin]

    def user_name(self, obj):
        return obj.__str__()

    def email(self, obj):
        return obj.user.email

admin.site.register(DoctorSpecialization)
admin.site.register(DoctorSubSpecialization)