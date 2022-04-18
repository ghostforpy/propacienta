from django.contrib import admin
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    ChronicDisease,
    DischargeEpicris,
    DischargeEpicrisFiles,
    DischargeEpicrisImage,
    Disease,
    TransferredDisease,
)


class EditMixin:
    extra = 0
    readonly_fields = ("get_edit_link",)

    def get_edit_link(self, obj=None):
        if (
            obj.pk
        ):  # if object has already been saved and has a primary key, show link to it
            url = reverse(
                "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
                args=[force_text(obj.pk)],
            )
            return format_html(
                '<a href="{url}">{text}</a>',
                url=url,
                # text=_("%s") % obj.__str__()
                text="Перейти на страницу",
            )

        return _("(save and continue editing to create a link)")

    get_edit_link.short_description = _("Просмотреть и изменить")
    get_edit_link.allow_tags = True


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
    search_fields = (
        "pacient__user__email",
        "pacient__user__last_name",
        "pacient__user__first_name",
        "pacient__user__patronymic",
        "pacient__phone",
    )


class DischargeEpicrisTabularAdmin(EditMixin, admin.StackedInline):
    model = DischargeEpicris
    fields = [
        "get_edit_link",
        "chronic_disease",
        "transferred_disease",
        "pacient",
        "d",
        "epicris",
    ]

    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super(DischargeEpicrisTabularAdmin, self).get_fieldsets(request, obj)
    #     fieldsets[0][1]['fields'] += ['get_edit_link']
    #     return fieldsets


@admin.register(ChronicDisease)
class ChronicDiseaseAdmin(admin.ModelAdmin):
    list_display = ("pacient", "disease")
    list_select_related = True
    inlines = [DischargeEpicrisTabularAdmin]
    list_filter = ("disease",)
    search_fields = (
        "pacient__user__email",
        "pacient__user__last_name",
        "pacient__user__first_name",
        "pacient__user__patronymic",
        "pacient__phone",
    )


@admin.register(TransferredDisease)
class TransferredDiseaseAdmin(admin.ModelAdmin):
    list_display = ("pacient", "disease")
    list_select_related = True
    inlines = [DischargeEpicrisTabularAdmin]
    list_filter = ("disease",)
    search_fields = (
        "pacient__user__email",
        "pacient__user__last_name",
        "pacient__user__first_name",
        "pacient__user__patronymic",
        "pacient__phone",
    )
