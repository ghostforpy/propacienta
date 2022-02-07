from pyexpat import model
from django.contrib import admin
from .models import Doctor
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from hospitals.models import Hospital

class HospitalModelAdmin(admin.TabularInline):
    model = Hospital


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
    list_display = ("user_name", "phone",)
    inlines = [UserModelAdmin]

    def user_name(self, obj):
        return obj.__str__()