from rest_framework import serializers

from ..models import MedicineCard


class MedicineCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCard
        exclude = ["id", "pacient"]
