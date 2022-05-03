from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from diseases.models import ChronicDisease, TransferredDisease
from medicine_cards.models import MedicineCard
from operations.models import TransferredOperation
from prescriptions.models import (
    AnalisisPrescription,
    MedicinePrescription,
    ProcedurePrescription,
)

from .models import Pacient


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


class TransferredOperationAdmin(EditMixin, admin.StackedInline):
    model = TransferredOperation
    fields = ["get_edit_link", "operation", "medicine_card", "effect", "date"]


class ChronicDiseaseAdmin(EditMixin, admin.StackedInline):
    model = ChronicDisease
    fields = ["get_edit_link", "disease", "medicine_card", "treatment"]


class TransferredDiseaseAdmin(EditMixin, admin.StackedInline):
    model = TransferredDisease
    fields = [
        "get_edit_link",
        "disease",
        "medicine_card",
        "diagnosis",
        "diagnosis_date",
        "diagnosis_year",
        "treatment_date",
        "treatment_end_date",
    ]


class ProcedurePrescriptionAdmin(EditMixin, admin.StackedInline):
    model = ProcedurePrescription
    fields = [
        "get_edit_link",
        "procedure",
        "medicine_card",
        "doctor",
        "doctor_appointment",
    ]


class AnalisisPrescriptionAdmin(EditMixin, admin.StackedInline):
    model = AnalisisPrescription
    fields = [
        "get_edit_link",
        "analisis",
        "medicine_card",
        "doctor",
        "doctor_appointment",
    ]


class MedicinePrescriptionAdmin(EditMixin, admin.StackedInline):
    model = MedicinePrescription
    fields = [
        "get_edit_link",
        "medicine",
        "medicine_card",
        "doctor",
        "doctor_appointment",
    ]


class UserModelAdmin(EditMixin, admin.StackedInline):
    model = get_user_model()
    fields = [
        "get_edit_link",
        "first_name",
        "last_name",
        "patronymic",
        "birthday",
        "email",
    ]


class MedicineCardModelAdmin(EditMixin, admin.StackedInline):
    model = MedicineCard
    fields = ["get_edit_link", "height", "weight", "average_pressure"]


@admin.register(Pacient)
class PacientAdmin(admin.ModelAdmin):
    search_fields = (
        "user__email",
        "user__last_name",
        "user__first_name",
        "user__patronymic",
        "phone",
    )
    list_display = (
        "email",
        "user_name",
        "phone",
    )
    list_select_related = True
    inlines = [
        UserModelAdmin,
        MedicineCardModelAdmin,
        TransferredOperationAdmin,
        ChronicDiseaseAdmin,
        TransferredDiseaseAdmin,
        ProcedurePrescriptionAdmin,
        AnalisisPrescriptionAdmin,
        MedicinePrescriptionAdmin,
    ]

    def user_name(self, obj):
        return obj.__str__()

    def email(self, obj):
        return obj.user.email

    # def change_view(self, request, object_id, form_url='', extra_context=None):

    #     print("change view")
    #     print(request, object_id, form_url, extra_context)
    #     return super().change_view(
    #         request, object_id, form_url, extra_context=extra_context,
    #     )

    # def add_view(request, form_url='', extra_context=None):
    #     print("add view")
    #     print(request, form_url, extra_context)
    #     return super().add_view(
    #         request, form_url, extra_context=extra_context,
    #     )

    # def get_queryset(self, request):
    #     """
    #     Return a QuerySet of all model instances that can be edited by the
    #     admin site. This is used by changelist_view.
    #     """
    #     print("get queryset")
    #     # qs = self.model._default_manager.get_queryset()
    #     qs = Pacient.objects.all().prefetch_related(
    #         "treating_doctors",
    #         "chronic_diseases",
    #         "transferred_diseases",
    #         "transferred_diseases__disease",
    #         # "transferred_diseases__disease"
    #     ).select_related("medicine_card", "user")
    #     # TODO: this should be handled by some parameter to the ChangeList.
    #     ordering = self.get_ordering(request)
    #     if ordering:
    #         qs = qs.order_by(*ordering)
    #     return qs
