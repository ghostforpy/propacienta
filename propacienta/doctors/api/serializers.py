from rest_framework import serializers

from doctors.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    # medicinecard = serializers.IntegerField(source="medicine_card.id")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    patronymic = serializers.CharField(source="user.patronymic")
    # birthday = serializers.DateField(source="user.birthday")
    treating_doctor = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = "__all__"

    def get_treating_doctor(self, obj):
        if self.context["view"].action == "list":
            if self.context["request"].user.is_authenticated:
                return obj.treating_doctor == 1
            return False
        else:
            if self.context["request"].user.is_authenticated:
                return (
                    obj in self.context["request"].user.pacient.treating_doctors.all()
                )
            return False
