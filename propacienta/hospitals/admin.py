from django.contrib import admin
from .models import Hospital, HospitalTown

# Register your models here.

admin.site.register(HospitalTown)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("title", "town", "address")
    search_fields = ["title", "town__title", "address"]
    list_filter = ("town",)
    list_select_related = ["town"]
