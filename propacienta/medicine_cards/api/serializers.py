from rest_framework import serializers
from ..models import MedicineCard, IndependentResearch, ResultIndependentResearch


class MedicineCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCard
        exclude = ["id", "pacient"]

class IndependentResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndependentResearch
        fields = "__all__"

class ResultIndependentResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultIndependentResearch
        fields = "__all__"