from django.contrib import admin
from .models import MedicinePrescription, ProcedurePrescription, AnalisisPrescription
# Register your models here.


class BasePrescriptionAdmin(admin.ModelAdmin):
    list_display = ("pacient", "doctor",)
    list_select_related = True

    def pacient(self, obj):
        return obj.medicine_card.pacient


@admin.register(MedicinePrescription)
class MedicinePrescriptionAdmin(BasePrescriptionAdmin):
    pass


@admin.register(ProcedurePrescription)
class ProcedurePrescriptionAdmin(BasePrescriptionAdmin):
    pass


@admin.register(AnalisisPrescription)
class AnalisisPrescriptionAdmin(BasePrescriptionAdmin):
    pass