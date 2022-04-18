from rest_framework import serializers

from pacients.models import Pacient


class PacientSerializer(serializers.ModelSerializer):
    medicinecard = serializers.IntegerField(source="medicine_card.id")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    patronymic = serializers.CharField(source="user.patronymic")
    birthday = serializers.DateField(source="user.birthday")

    class Meta:
        model = Pacient
        fields = [
            "id",
            "medicinecard",
            "first_name",
            "last_name",
            "patronymic",
            "birthday",
            "phone",
        ]
