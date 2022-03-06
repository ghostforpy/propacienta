from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreatePasswordRetypeSerializer
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    #api_url = serializers.CharField(source="get_api_url")
    # url = serializers.CharField(source="get_absolute_url")
    doc_mode_available = serializers.SerializerMethodField()
    pacient_phone = serializers.CharField(source="pacient.phone")
    doctor_phone = serializers.SerializerMethodField()
    pacient_id = serializers.IntegerField(source="pacient.id")
    doctor_id = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "first_name", 
            "last_name", 
            "email", 
            "patronymic", 
            "id",
            #"api_url",
            #"url",
            "birthday",
            "doc_mode_available",
            "pacient_phone",
            "doctor_phone",
            "pacient_id",
            "doctor_id"
        ]

        #extra_kwargs = {
        #    "url": {"view_name": "api:users-detail", "lookup_field": "id"}
        #}
    def get_doc_mode_available(self, obj):
        if obj.doctor != None:
            if obj.doctor.is_active:
                return True
        return False

    def get_doctor_phone(self, obj):
        if obj.doctor != None:
            if obj.doctor.is_active:
                return obj.doctor.phone

    def get_doctor_id(self, obj):
        if obj.doctor != None:
            if obj.doctor.is_active:
                return obj.doctor.id


class CUserCreateSerializer(UserCreatePasswordRetypeSerializer):

    role_doctor = serializers.BooleanField(write_only=True)
    
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = tuple(UserCreatePasswordRetypeSerializer.Meta.fields) + ('role_doctor',)
    
    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def validate(self, attrs):
        _ = attrs.pop("role_doctor", False)
        return super().validate(attrs)