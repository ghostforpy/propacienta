from django.contrib import admin
from .models import MedicineCard, IndependentResearch, ResultIndependentResearch
# Register your models here.


admin.site.register(IndependentResearch)

class ResultIndependentResearchAdmin(admin.TabularInline):
    model = ResultIndependentResearch

@admin.register(MedicineCard)
class MedicineCardAdmin(admin.ModelAdmin):
    list_display = ("user_name",)
    inlines = [ResultIndependentResearchAdmin]

    def user_name(self, obj):
        return obj.pacient.__str__()