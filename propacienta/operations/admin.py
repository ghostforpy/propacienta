from django.contrib import admin
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    Operation,
    TransferredOperation,
    TransferredOperationFile,
    TransferredOperationImage,
)

# class EditMixin:
#     extra = 0
#     readonly_fields = ("get_edit_link",)

#     def get_edit_link(self, obj=None):
#         if (
#             obj.pk
#         ):  # if object has already been saved and has a primary key, show link to it
#             url = reverse(
#                 "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
#                 args=[force_text(obj.pk)],
#             )
#             return format_html(
#                 '<a href="{url}">{text}</a>',
#                 url=url,
#                 # text=_("%s") % obj.__str__()
#                 text="Перейти на страницу",
#             )

#         return _("(save and continue editing to create a link)")

#     get_edit_link.short_description = _("Просмотреть и изменить")
#     get_edit_link.allow_tags = True


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title",)


# @admin.register(TransferredOperationFile)
# class TransferredOperationFileAdmin(admin.ModelAdmin):
#     list_display = ("transferred_operation",)


# @admin.register(TransferredOperationImage)
# class TransferredOperationImageAdmin(admin.ModelAdmin):
#     list_display = ("transferred_operation",)


class TransferredOperationFileAdminTabular(admin.TabularInline):
    model = TransferredOperationFile


class TransferredOperationImageAdminTabular(admin.TabularInline):
    model = TransferredOperationImage


@admin.register(TransferredOperation)
class TransferredOperationAdmin(admin.ModelAdmin):
    list_display = ("pacient", "operation", "date")
    list_select_related = True
    inlines = [TransferredOperationFileAdminTabular, TransferredOperationImageAdminTabular]
    list_filter = ("operation",)
    search_fields = (
        "pacient__user__email",
        "pacient__user__last_name",
        "pacient__user__first_name",
        "pacient__user__patronymic",
        "pacient__phone",
    )
