from django.contrib import admin

from .models import IndependentResearch, MedicineCard, ResultIndependentResearch

admin.site.register(IndependentResearch)


class ResultIndependentResearchAdmin(admin.TabularInline):
    model = ResultIndependentResearch


@admin.register(MedicineCard)
class MedicineCardAdmin(admin.ModelAdmin):
    search_fields = (
        "pacient__user__email",
        "pacient__user__last_name",
        "pacient__user__first_name",
        "pacient__user__patronymic",
        "pacient__phone",
    )
    list_filter = ("gender", "blood_type")
    list_display = ("user_name",)
    inlines = [ResultIndependentResearchAdmin]

    def user_name(self, obj):
        return obj.pacient.__str__()
