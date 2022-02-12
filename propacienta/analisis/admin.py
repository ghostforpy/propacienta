from django.contrib import admin
from .models import Analysis, AnalysisResult, AnalysisResultsFile, AnalysisResultsImage
# Register your models here.

admin.site.register(Analysis)

class AnalysisResultsFileAdmin(admin.TabularInline):
    model = AnalysisResultsFile


class AnalysisResultsImageAdmin(admin.TabularInline):
    model = AnalysisResultsImage

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ("pacient", "analysis",)
    list_select_related = True
    inlines = [AnalysisResultsFileAdmin, AnalysisResultsImageAdmin]
