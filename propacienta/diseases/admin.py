from django.contrib import admin
from .models import Disease, ChronicDisease, DischargeEpicris, DischargeEpicrisImage, DischargeEpicrisFiles
# Register your models here.

admin.site.register(Disease)


class DischargeEpicrisFilesAdmin(admin.TabularInline):
    model = DischargeEpicrisFiles


class DischargeEpicrisImageAdmin(admin.TabularInline):
    model = DischargeEpicrisImage


@admin.register(DischargeEpicris)
class DischargeEpicrisAdmin(admin.ModelAdmin):
    list_display = ("pacient", "chronic_disease", "d")
    list_select_related = True
    inlines = [DischargeEpicrisImageAdmin, DischargeEpicrisFilesAdmin]

class DischargeEpicrisTabularAdmin(admin.TabularInline):
    model = DischargeEpicris

@admin.register(ChronicDisease)
class ChronicDiseaseAdmin(admin.ModelAdmin):
    list_display = ("pacient", "disease")
    list_select_related = True
    inlines = [DischargeEpicrisTabularAdmin]