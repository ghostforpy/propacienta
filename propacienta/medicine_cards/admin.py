from django.contrib import admin
from .models import MedicineCard
# Register your models here.

@admin.register(MedicineCard)
class PacientAdmin(admin.ModelAdmin):
    list_display = ("user_name",)
    #inlines = [UserModelAdmin, MedicineCardModelAdmin]

    def user_name(self, obj):
        return obj.pacient.__str__()