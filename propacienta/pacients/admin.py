from select import select
from django.contrib import admin
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from medicine_cards.models import MedicineCard
from operations.models import TransferredOperation
from prescriptions.models import ProcedurePrescription, AnalisisPrescription, MedicinePrescription
from diseases.models import ChronicDisease, TransferredDisease
from .models import Pacient


class EditMixin:
    extra = 0
    readonly_fields = ('get_edit_link',)
    def get_edit_link(self, obj=None):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return """<a href="{url}">{text}</a>""".format(
                url=url,
                text=_("Edit this %s separately") % obj._meta.verbose_name,
            )
        return _("(save and continue editing to create a link)")
    get_edit_link.short_description = _("Просмотреть и изменить")
    get_edit_link.allow_tags = True


class TransferredOperationAdmin(EditMixin, admin.StackedInline):
    model = TransferredOperation
    fields = ['get_edit_link', "operation", "medicine_card", "effect", "date"]


class ChronicDiseaseAdmin(EditMixin, admin.StackedInline):
    model = ChronicDisease
    fields = ['get_edit_link', "disease", "medicine_card", "treatment"]

class TransferredDiseaseAdmin(EditMixin, admin.StackedInline):
    model = TransferredDisease
    fields = ['get_edit_link', "disease", "medicine_card",
                "diagnosis", "diagnosis_date", "diagnosis_year",
                "treatment_date", "treatment_end_date"]

class ProcedurePrescriptionAdmin(EditMixin, admin.StackedInline):
    model = ProcedurePrescription
    fields = ['get_edit_link', "procedure", "medicine_card", "doctor", "doctor_appointment"]


class AnalisisPrescriptionAdmin(EditMixin, admin.StackedInline):
    model = AnalisisPrescription
    fields = ['get_edit_link', "analisis", "medicine_card", "doctor", "doctor_appointment"]

class MedicinePrescriptionAdmin(EditMixin, admin.StackedInline):
    model = MedicinePrescription
    fields = ['get_edit_link', "medicine", "medicine_card", "doctor", "doctor_appointment"]


class UserModelAdmin(admin.StackedInline):
    model = get_user_model()
    fields = [
        "first_name",
        "last_name",
        "patronymic",
        "birthday"
    ]

class MedicineCardModelAdmin(admin.StackedInline):
    model = MedicineCard
    #fields = [
    #    "first_name",
    #    "last_name",
    #    "patronymic",
    #    "birthday"
    #]

# Register your models here.
@admin.register(Pacient)
class PacientAdmin(admin.ModelAdmin):
    list_display = ("user_name", "phone",)
    list_select_related = True
    inlines = [
        UserModelAdmin,
        MedicineCardModelAdmin,
        TransferredOperationAdmin,
        ChronicDiseaseAdmin,
        TransferredDiseaseAdmin,
        ProcedurePrescriptionAdmin,
        AnalisisPrescriptionAdmin,
        MedicinePrescriptionAdmin
        ]

    def user_name(self, obj):
        return obj.__str__()