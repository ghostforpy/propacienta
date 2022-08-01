# from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
# from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from doctors.utils import request_by_doctor

from ..models import Dialog, DialogMessage

# from propacienta.users.models import User


# from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()
channel_layer = get_channel_layer()

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


class CreateDialogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pacient_id",
            "doctor_id",
        ]


class DialogSerializer(serializers.ModelSerializer):
    members = DialogUserSerializer(many=True, read_only=True)
    dialog_is_not_empty = serializers.BooleanField(read_only=True)
    opponent_id = serializers.IntegerField(write_only=True)
    opponent_type = serializers.CharField(write_only=True)
    messages__count = serializers.IntegerField(read_only=True)
    last = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Dialog
        fields = "__all__"

    def create(self, validated_data):
        try:
            first_member, second_member = validated_data["members"]
            dialog = Dialog.objects.filter(members=first_member).filter(members=second_member).get()
            return dialog
        except Dialog.DoesNotExist:
            instance = super().create(validated_data)
            # уведомление другого пользователя о созданном чате
            instance.dialog_is_not_empty = False
            serializer = DialogSerializer(instance)
            async_to_sync(channel_layer.group_send)(
                str(second_member.id),
                {
                    "type": "send.json",
                    "content": {
                        "type": "service",
                        "service_type": "newchat",
                        "chat": serializer.data
                    },
                },
            )
            return instance

    def validate_opponent_type(self, value):
        if value not in ["pacient", "doctor"]:
            raise serializers.ValidationError("Wrong opponent_type.")
        else:
            return value

    def validate(self, attrs):
        opponent_type = attrs.pop("opponent_type")
        opponent_id = attrs.pop("opponent_id")
        first_member = self.context["request"].user
        try:
            second_member = User.objects.get(
                **{
                    "{}__id".format(opponent_type): opponent_id
                }
            )
        except User.DoesNotExist:
            raise serializers.ValidationError("Wrong opponent.")
        except Exception:
            raise serializers.ValidationError("Bad request.")
        dialog_count = Dialog.objects.filter(
            members=first_member
            ).filter(members=second_member).count()
        if dialog_count > 1:
            raise serializers.ValidationError("Multiple dialogs")
        if opponent_type == "pacient":
            doctor = request_by_doctor(self.context["request"])
            if doctor != first_member.doctor:
                raise PermissionDenied
            if doctor not in second_member.pacient.treating_doctors.all():
                raise PermissionDenied
        else:
            if second_member.doctor is None:
                raise serializers.ValidationError("Wrong opponent.")
            if second_member.doctor not in first_member.pacient.treating_doctors.all():
                raise PermissionDenied
        attrs["members"] = (first_member, second_member)
        return super().validate(attrs)


class DialogMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = DialogMessage
        fields = "__all__"
