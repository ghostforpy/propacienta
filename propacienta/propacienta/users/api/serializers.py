from traceback import print_tb
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.mixins import UpdateModelMixin
from djoser.serializers import UserCreatePasswordRetypeSerializer
from doctors.models import Doctor
from pacients.models import Pacient

User = get_user_model()


class CUserSerializer(serializers.ModelSerializer):
    # api_url = serializers.CharField(source="get_api_url")
    # url = serializers.CharField(source="get_absolute_url")
    doc_mode_available = serializers.SerializerMethodField()
    pacient_phone = serializers.SerializerMethodField()
    doctor_phone = serializers.SerializerMethodField()
    phone_pacient = serializers.CharField(write_only=True)
    phone_doctor = serializers.CharField(write_only=True)
    pacient_id = serializers.IntegerField(source="pacient.id")
    doctor_id = serializers.SerializerMethodField()
    medicine_card = serializers.IntegerField(source="pacient.medicine_card.id")

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "patronymic",
            "id",
            # "api_url",
            # "url",
            "birthday",
            "doc_mode_available",
            "pacient_phone",
            "doctor_phone",
            "pacient_id",
            "doctor_id",
            "phone_pacient",
            "phone_doctor",
            "medicine_card",
        ]

        # extra_kwargs = {
        #    "url": {"view_name": "api:users-detail", "lookup_field": "id"}
        # }

    def get_doc_mode_available(self, obj):
        if obj.doctor != None:
            if obj.doctor.is_active:
                return True
        return False

    def get_pacient_phone(self, obj):
        return obj.pacient.phone

    def get_doctor_phone(self, obj):
        if obj.doctor != None:
            if obj.doctor.is_active:
                return obj.doctor.phone

    def get_doctor_id(self, obj):
        if obj.doctor != None:
            if obj.doctor.is_active:
                return obj.doctor.id

    # дописать валидацию телефонов

    def save(self, *args, **kwargs):
        print(self.validated_data)
        if "phone_pacient" in self.validated_data:
            self.instance.pacient.phone = self.validated_data["phone_pacient"]
            self.instance.pacient.save()
        if "phone_doctor" in self.validated_data:
            self.instance.doctor.phone = self.validated_data["phone_doctor"]
            self.instance.doctor.save()
        return super().save(*args, **kwargs)


class CUserCreateSerializer(UserCreatePasswordRetypeSerializer):

    role_doctor = serializers.BooleanField(write_only=True)
    phone_doctor = serializers.CharField(max_length=30, required=False, allow_null=True)
    phone_pacient = serializers.CharField(max_length=30, required=True, allow_null=True)

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = tuple(UserCreatePasswordRetypeSerializer.Meta.fields) + (
            "role_doctor",
            "phone_doctor",
            "phone_pacient",
        )

    def save(self, **kwargs):
        return super().save(**kwargs)

    def validate(self, attrs):
        role_doctor = attrs.pop("role_doctor", False)
        _ = attrs.pop("phone_pacient", "")
        phone_doctor = attrs.pop("phone_doctor", "")
        if role_doctor:
            if phone_doctor is None:
                raise serializers.ValidationError(
                    "Поле телефона доктора является обязательным."
                )
        return super().validate(attrs)

    def validate_phone_doctor(self, value):
        """
        Проверка телефона доктора.
        """
        if value is not None:
            # добавить валидацию
            if Doctor.objects.filter(phone=value).exists():
                raise serializers.ValidationError(
                    "Доктор с таким телефоном уже существует."
                )
        return value

    def validate_phone_pacient(self, value):
        """
        Проверка телефона пациента.
        """
        if value is not None:
            # добавить валидацию
            if Pacient.objects.filter(phone=value).exists():
                raise serializers.ValidationError(
                    "Пациент с таким телефоном уже существует."
                )
        else:
            raise serializers.ValidationError("Поле телефона является обязательным.")
        return value
