from django.contrib import admin

from .models import Analysis, AnalysisResult, AnalysisResultsFile, AnalysisResultsImage

# Register your models here.


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ["title", "diseases__title"]


class AnalysisResultsFileAdmin(admin.TabularInline):
    model = AnalysisResultsFile


class AnalysisResultsImageAdmin(admin.TabularInline):
    model = AnalysisResultsImage


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = (
        "pacient",
        "analysis",
    )
    list_select_related = True
    inlines = [AnalysisResultsFileAdmin, AnalysisResultsImageAdmin]
    list_filter = ("analysis",)
    search_fields = (
        "pacient__user__email",
        "pacient__user__last_name",
        "pacient__user__first_name",
        "pacient__user__patronymic",
        "pacient__phone",
    )
