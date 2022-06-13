from django import forms
from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from .models import Dialog, DialogMessage


class DialogAdminForm(forms.ModelForm):
    def clean_members(self):
        members = self.cleaned_data['members']
        if len(members) != 2:
            raise forms.ValidationError(_('В диалоге должно быть 2 участника'))
        dialog = Dialog.objects.annotate(
            num_members=Count('members')
        ).filter(
            num_members=2
        ).filter(
            members__in=[members[0]]
        ).filter(
            members__in=[members[1]]
        ).exists()
        if dialog:
            raise forms.ValidationError(_('Диалог с такими участниками уже существует'))
        return members

    class Meta:
        model = Dialog
        fields = '__all__'


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    form = DialogAdminForm


@admin.register(DialogMessage)
class DialogMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "created_at", "dialog_id", "received_by_the_user", "read_by_the_user")

    def dialog_id(self, obj):
        return obj.dialog.id
