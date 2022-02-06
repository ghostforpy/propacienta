from django.contrib import admin
from .models import Pacient
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from medicine_cards.models import MedicineCard

class UserModelAdmin(admin.StackedInline):
    model = get_user_model()
    fields = [
        "first_name",
        "last_name",
        "patronymic",
        "birthday"
    ]

class MedicineCardModelAdmin(admin.StackedInline):
    model = MedicineCard
    #fields = [
    #    "first_name",
    #    "last_name",
    #    "patronymic",
    #    "birthday"
    #]

# Register your models here.
@admin.register(Pacient)
class PacientAdmin(admin.ModelAdmin):
    list_display = ("user_name", "phone",)
    inlines = [UserModelAdmin, MedicineCardModelAdmin]

    def user_name(self, obj):
        return obj.__str__()