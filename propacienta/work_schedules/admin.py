from django import forms
from django.contrib import admin

from .models import NotWorkingPeriod, WorkDay


class WorkDayAdminForm(forms.ModelForm):

    time_field = forms.CharField(initial="00:00-00:00", label="Перерыв")

    # def save(self, commit=True):
    #     extra_field = self.cleaned_data.get('extra_field', None)
    #     return super(WorkDayAdminForm, self).save(commit=commit)

    class Meta:
        model = WorkDay
        fields = "__all__"

@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    form = WorkDayAdminForm
    search_fields = (
        "doctor__user__email",
        "doctor__user__last_name",
        "doctor__user__first_name",
        "doctor__user__patronymic",
    )
    list_display = (
        "date",
        "doctor",
        "hospital",
    )
    list_select_related = True
    list_filter = ("hospital", "date")
    readonly_fields = ("timeslotmask", "have_a_rest_timeslotmask")
    fieldsets = (
        (None, {
            'fields': ('date', 'doctor', 'since', 'to', 'hospital', 'appointment_duration'),
        }),
        ('Перерывы', {
            # 'classes': ('wide',),
            'fields': ('breaks', 'time_field'),
        }),
        ('Маски', {
            'classes': ('collapse',),
            'fields': ('timeslotmask', 'have_a_rest_timeslotmask'),
        })
    )

    # class Media:
    #     js = ("js/work_schedules/admin_form.js",)


@admin.register(NotWorkingPeriod)
class NotWorkingPeriodAdmin(admin.ModelAdmin):
    search_fields = (
        "doctor__user__email",
        "doctor__user__last_name",
        "doctor__user__first_name",
        "doctor__user__patronymic",
    )
    list_display = (
        "doctor",
        "since",
        "to",
        "is_open",
    )
    list_select_related = True
    list_filter = ("is_open", "hospital", "reason",)
