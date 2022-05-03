from rest_framework import serializers

from doctors.models import Doctor, DoctorSpecialization, DoctorSubSpecialization


class DoctorSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSpecialization
        fields = "__all__"


class DoctorSubSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSubSpecialization
        fields = "__all__"


class DoctorSpecializationListSerializer(serializers.ModelSerializer):
    sub_specializations = DoctorSubSpecializationSerializer(many=True)

    class Meta:
        model = DoctorSpecialization
        fields = "__all__"


class DoctorUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Doctor
        exclude = ["hospitals"]
        extra_kwargs = {
            "is_active": {"read_only": True},
            "phone": {"write_only": True, "required": False},
        }


class DoctorSerializer(serializers.ModelSerializer):
    # medicinecard = serializers.IntegerField(source="medicine_card.id")
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    patronymic = serializers.CharField(source="user.patronymic", read_only=True)
    # birthday = serializers.DateField(source="user.birthday")
    treating_doctor = serializers.SerializerMethodField()
    specializations = DoctorSpecializationSerializer(many=True)
    sub_specializations = DoctorSubSpecializationSerializer(many=True)

    class Meta:
        model = Doctor
        exclude = ["hospitals"]
        # extra_kwargs = {
        #    "is_active": {"read_only": True}, "phone": {"write_only": True, "required": False}
        # }

    def get_treating_doctor(self, obj):
        if self.context["view"].action == "list":
            if self.context["request"].user.is_authenticated:
                return obj.treating_doctor == 1
            return False
        elif self.context["view"].action == "retrieve":
            if self.context["request"].user.is_authenticated:
                return self.context["request"].user.pacient in obj.pacients.all()
            return False
        return False
