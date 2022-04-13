from django.contrib import admin

from .models import (
    ChronicDisease,
    DischargeEpicris,
    DischargeEpicrisFiles,
    DischargeEpicrisImage,
    Disease,
    TransferredDisease,
)


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
    list_filter = ("chronic_disease__disease",)
    inlines = [DischargeEpicrisImageAdmin, DischargeEpicrisFilesAdmin]
    search_fields = ("pacient__user__email", "pacient__user__last_name",
                    "pacient__user__first_name", "pacient__user__patronymic",
                    "pacient__phone",)


class DischargeEpicrisTabularAdmin(admin.TabularInline):
    model = DischargeEpicris


@admin.register(ChronicDisease)
class ChronicDiseaseAdmin(admin.ModelAdmin):
    list_display = ("pacient", "disease")
    list_select_related = True
    inlines = [DischargeEpicrisTabularAdmin]
    list_filter = ("disease",)
    search_fields = ("pacient__user__email", "pacient__user__last_name",
                    "pacient__user__first_name", "pacient__user__patronymic",
                    "pacient__phone",)


@admin.register(TransferredDisease)
class TransferredDiseaseAdmin(admin.ModelAdmin):
    list_display = ("pacient", "disease")
    list_select_related = True
    #inlines = [DischargeEpicrisTabularAdmin]
    list_filter = ("disease",)
    search_fields = ("pacient__user__email", "pacient__user__last_name",
                    "pacient__user__first_name", "pacient__user__patronymic",
                    "pacient__phone",)
