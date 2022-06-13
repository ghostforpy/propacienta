# from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
# from django.db.models import Q
from rest_framework import serializers

from ..models import Dialog, DialogMessage

# from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class DialogUserSerializer(serializers.ModelSerializer):
    pacient_id = serializers.IntegerField(source="pacient.id")
    doctor_id = serializers.SerializerMethodField()
    doctor_foto = serializers.SerializerMethodField()
    medicine_card = serializers.IntegerField(source="pacient.medicine_card.id")
    fio = serializers.CharField(source="get_fio")

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "patronymic",
            "id",
            "pacient_id",
            "doctor_id",
            "medicine_card",
            "fio",
            "doctor_foto"
        ]

    def get_doctor_id(self, obj):
        if obj.doctor is not None:
            if obj.doctor.is_active:
                return obj.doctor.id

    def get_doctor_foto(self, obj):
        if obj.doctor is not None:
            if obj.doctor.is_active:
                return obj.doctor.avatar.url


class DialogSerializer(serializers.ModelSerializer):
    members = DialogUserSerializer(many=True)
    messages__count = serializers.IntegerField()
    last = serializers.DateTimeField()

    class Meta:
        model = Dialog
        fields = "__all__"


class DialogMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = DialogMessage
        fields = "__all__"
