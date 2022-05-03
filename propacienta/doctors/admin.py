from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Doctor, DoctorSpecialization, DoctorSubSpecialization

# from hospitals.models import Hospital


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


class UserModelAdmin(EditMixin, admin.StackedInline):
    model = get_user_model()
    fields = ["get_edit_link", "first_name", "last_name", "patronymic", "birthday"]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "user_name",
        "phone",
        "is_active",
    )
    inlines = [UserModelAdmin]
    search_fields = (
        "user__email",
        "user__last_name",
        "user__first_name",
        "user__patronymic",
        "phone",
    )
    list_select_related = True
    list_filter = ("is_active", "specializations", "sub_specializations", "hospitals")

    def user_name(self, obj):
        return obj.__str__()

    def email(self, obj):
        return obj.user.email


@admin.register(DoctorSpecialization)
class DoctorSpecializationAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(DoctorSubSpecialization)
class DoctorSubSpecializationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "specialization",
    )
    search_fields = (
        "title",
        "specialization__title",
    )
    list_filter = ("specialization",)
