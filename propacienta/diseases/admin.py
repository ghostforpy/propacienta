from django.contrib import admin
from .models import (Disease, ChronicDisease, DischargeEpicris,
                     DischargeEpicrisImage, DischargeEpicrisFiles,
                     TransferredDisease)
# Register your models here.

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    search_fields = ["title", "code"]
    list_display = ("title", "code")


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


@admin.register(TransferredDisease)
class TransferredDiseaseAdmin(admin.ModelAdmin):
    list_display = ("pacient", "disease")
    list_select_related = True
    #inlines = [DischargeEpicrisTabularAdmin]