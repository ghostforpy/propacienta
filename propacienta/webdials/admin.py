from django.contrib import admin

from .models import WebDial

# Register your models here.


@admin.register(WebDial)
class WebDialAdmin(admin.ModelAdmin):
    search_fields = (
        "initiator__email",
        "initiator__last_name",
        "initiator__first_name",
        "initiator__patronymic",
        "opponent__email",
        "opponent__last_name",
        "opponent__first_name",
        "opponent__patronymic",
    )
    list_display = (
        "initiator",
        "opponent",
        "start_webdial",
        "end_webdial",
        "webdial_duration",
        "end_webdial_reason",
    )
    list_filter = ("webdial_happen", "end_webdial_reason")
