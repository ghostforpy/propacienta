from django.contrib import admin
from .models import AppointmentOrder, AppointmentSurvey, DoctorAppointment
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(AppointmentOrder)
class AppointmentOrderAdmin(admin.ModelAdmin):
    list_display = (
        "pacient", "doctor", "dt", "confirmation",
        "appointment_took_place", "hospital",
    )
    date_hierarchy = "dt"
    list_filter = ("confirmation", "appointment_took_place", "hospital",)
    list_select_related = True

@admin.register(AppointmentSurvey)
class AppointmentSurveyAdmin(admin.ModelAdmin):
    list_display = (
        "appointment_order",
    )

@admin.register(DoctorAppointment)
class DoctorAppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "pacient", "doctor", "dt", "hospital", "rating_for_pacient", "rating_for_doctor",
    )
    date_hierarchy = "dt"
    list_filter = ("hospital",)
    list_select_related = True