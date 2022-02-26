from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreatePasswordRetypeSerializer
User = get_user_model()


class UserSerializerz(serializers.ModelSerializer):
    api_url = serializers.CharField(source="get_api_url")
    url = serializers.CharField(source="get_absolute_url")
    class Meta:
        model = User
        fields = ["name", "api_url", "url"]

        #extra_kwargs = {
        #    "url": {"view_name": "api:users-detail", "lookup_field": "id"}
        #}


class CUserCreateSerializer(UserCreatePasswordRetypeSerializer):

    role_doctor = serializers.BooleanField(write_only=True)
    
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = tuple(UserCreatePasswordRetypeSerializer.Meta.fields) + ('role_doctor',)
    
    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def validate(self, attrs):
        _ = attrs.pop("role_doctor", False)
        return super().validate(attrs)