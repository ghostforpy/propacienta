from django.contrib import admin
from .models import Operation, TransferredOperation

# Register your models here.

admin.site.register(Operation)


@admin.register(TransferredOperation)
class TransferredOperationAdmin(admin.ModelAdmin):
    list_display = ("pacient", "operation", "date")
    list_select_related = True
