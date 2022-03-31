from itertools import count
from rest_framework import serializers
from ..models import Analysis, AnalysisResult, AnalysisResultsFile, AnalysisResultsImage


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = "__all__"


class AnalysisSimpleSerializer(serializers.ModelSerializer):
    # results_count = serializers.SerializerMethodField()
    results_count = serializers.IntegerField(default=0)
    class Meta:
        model = Analysis
        exclude = ["diseases"]

    # def get_results_count(self, obj):
    #     queryparams = self.context["request"].GET.dict()
    #     pacient_id = queryparams.get("pacientId", None)
    #     if pacient_id is not None:
    #         count = AnalysisResult.objects.filter(
    #             analysis=obj
    #             ).filter(
    #                 pacient__id=pacient_id
    #                 ).count()
    #         if count > 0:
    #             return count
    #     return 0


class AnalysisResultsFileSerializer(serializers.ModelSerializer):
    """Сериалайзер для файлов результатов анализов"""

    file = serializers.CharField(source="file.url")
    delete_url = serializers.CharField(source="get_absolute_url")

    class Meta:
        model = AnalysisResultsFile
        exclude = ["analysis_result", "id"]


class AnalysisResultsImageSerializer(serializers.ModelSerializer):
    """Сериалайзер для изображений результатов анализов"""

    image = serializers.CharField(source="image.url")
    delete_url = serializers.CharField(source="get_absolute_url")

    class Meta:
        model = AnalysisResultsImage
        exclude = ["analysis_result", "id"]


class AnalysisResultSerializer(serializers.ModelSerializer):
    analysis_files = AnalysisResultsFileSerializer(many=True, required=False)
    analysis_images = AnalysisResultsImageSerializer(many=True, required=False)

    class Meta:
        model = AnalysisResult
        fields = "__all__"

    def create(self, validated_data):
        images_data = self.context["request"].data.getlist("images")
        files_data = self.context["request"].data.getlist("files")
        analysis_result = AnalysisResult.objects.create(**validated_data)
        # if instance.images.count() + len(images_data) > MAXIMUM_SERVICES_IMAGES_COUNT:
        #     raise ValidationError(
        #         "Maximum count of images is {}".format(MAXIMUM_SERVICES_IMAGES_COUNT)
        #     )
        for image_data in images_data:
            # сохранянем изображения
            AnalysisResultsImage.objects.create(
                analysis_result=analysis_result, 
                image=image_data
            )
        for file_data in files_data:
            # сохранянем файлы
            AnalysisResultsFile.objects.create(
                analysis_result=analysis_result, 
                file=file_data
            )
        analysis_result.save()
        return analysis_result