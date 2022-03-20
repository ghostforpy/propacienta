from rest_framework import serializers
from ..models import Analysis, AnalysisResult, AnalysisResultsFile, AnalysisResultsImage


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = "__all__"

class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = "__all__"

class AnalysisResultsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResultsFile
        fields = "__all__"

class AnalysisResultsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResultsImage
        fields = "__all__"