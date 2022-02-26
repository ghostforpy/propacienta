from django.contrib.auth import get_user_model
from rest_framework import serializers

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
