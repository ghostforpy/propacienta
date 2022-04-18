from rest_framework import serializers

from ..models import (
    ChronicDisease,
    DischargeEpicris,
    DischargeEpicrisFiles,
    DischargeEpicrisImage,
    Disease,
    TransferredDisease,
)


class ValidatePacientIdMixin:
    def validate_pacient(self, value):
        pacient_id = self.context['view'].kwargs["pacient_id"]
        if value.id != pacient_id:
            raise serializers.ValidationError("Wrong pacientId.")
        return value


class DiseaseSerializer(serializers.ModelSerializer):
    diseases_count = serializers.IntegerField(default=0)

    class Meta:
        model = Disease
        fields = "__all__"


class ChronicDiseaseSerializer(serializers.ModelSerializer):
    disease_title = serializers.CharField(read_only=True, source="disease.title")

    class Meta:
        model = ChronicDisease
        exclude = ["medicine_card", "pacient"]


class DischargeEpicrisFilesSerializer(serializers.ModelSerializer):
    """Сериалайзер для файлов выписных эпикризов хронических заболеваний."""

    file = serializers.CharField(source="file.url")
    delete_url = serializers.CharField(source="get_absolute_url")

    class Meta:
        model = DischargeEpicrisFiles
        exclude = ["discharge_epicris", "id"]


class DischargeEpicrisImageSerializer(serializers.ModelSerializer):
    """Сериалайзер для изображений выписных эпикризов хронических заболеваний."""

    image = serializers.CharField(source="image.url")
    delete_url = serializers.CharField(source="get_absolute_url")

    class Meta:
        model = DischargeEpicrisImage
        exclude = ["discharge_epicris", "id"]


class DischargeEpicrisSerializer(ValidatePacientIdMixin, serializers.ModelSerializer):
    """Сериалайзер для выписного эпикриза хронического или перенесённого заболевания."""
    discharge_epicrisis_files = DischargeEpicrisFilesSerializer(many=True, required=False)
    discharge_epicrisis_images = DischargeEpicrisImageSerializer(many=True, required=False)
    disease = serializers.IntegerField(write_only=True)

    class Meta:
        model = DischargeEpicris
        fields = "__all__"
        extra_kwargs = {
            'chronic_disease': {'required': False},
            'transferred_disease': {'required': False}
        }

    def validate_disease(self, value):
        try:
            disease = Disease.objects.get(id=value)
            return disease
        except Disease.DoesNotExist:
            raise serializers.ValidationError("Wrong diseaseId.")

    def create(self, validated_data):
        images_data = self.context["request"].data.getlist("images")
        files_data = self.context["request"].data.getlist("files")
        disease = validated_data.pop("disease")
        pacient = validated_data["pacient"]
        chronic_disease, _ = ChronicDisease.objects.get_or_create(
            disease=disease,
            pacient=pacient,
            medicine_card=pacient.medicine_card
        )
        discharge_epicris = DischargeEpicris.objects.create(
            chronic_disease=chronic_disease, **validated_data
        )
        # if instance.images.count() + len(images_data) > MAXIMUM_SERVICES_IMAGES_COUNT:
        #     raise ValidationError(
        #         "Maximum count of images is {}".format(MAXIMUM_SERVICES_IMAGES_COUNT)
        #     )
        for image_data in images_data:
            # сохранянем изображения
            DischargeEpicrisImage.objects.create(
                discharge_epicris=discharge_epicris, 
                image=image_data
            )
        for file_data in files_data:
            # сохранянем файлы
            DischargeEpicrisFiles.objects.create(
                discharge_epicris=discharge_epicris, 
                file=file_data
            )
        discharge_epicris.save()
        return discharge_epicris


class TransferredDiseaseSerializer(ValidatePacientIdMixin, serializers.ModelSerializer):
    disease_title = serializers.CharField(read_only=True, source="disease.title")
    discharge_epicris = DischargeEpicrisSerializer(read_only=True)
    epicris = serializers.CharField(write_only=True, required=False)
    epicris_date = serializers.DateField(write_only=True, required=False)

    class Meta:
        model = TransferredDisease
        fields = "__all__"

    def validate(self, data):
        """
        Check dates.
        """
        if not (data['diagnosis_date'] < data['treatment_date'] < data['treatment_end_date']):
            raise serializers.ValidationError("Wrong dates")
        return data

    def create(self, validated_data):
        images_data = self.context["request"].data.getlist("images")
        files_data = self.context["request"].data.getlist("files")
        epicris = validated_data.pop("epicris", None)
        epicris_date = validated_data.pop("epicris_date", None)
        transferred_disease = TransferredDisease.objects.create(**validated_data)
        if not (
            epicris is None and epicris_date is None and len(images_data) == 0 and len(files_data) == 0
        ):
            discharge_epicris = DischargeEpicris.objects.create(
                transferred_disease=transferred_disease,
                pacient=validated_data["pacient"],
                epicris=epicris,
                d=epicris_date or validated_data["treatment_end_date"]
            )
            # if instance.images.count() + len(images_data) > MAXIMUM_SERVICES_IMAGES_COUNT:
            #     raise ValidationError(
            #         "Maximum count of images is {}".format(MAXIMUM_SERVICES_IMAGES_COUNT)
            #     )
            for image_data in images_data:
                # сохранянем изображения
                DischargeEpicrisImage.objects.create(
                    discharge_epicris=discharge_epicris, 
                    image=image_data
                )
            for file_data in files_data:
                # сохранянем файлы
                DischargeEpicrisFiles.objects.create(
                    discharge_epicris=discharge_epicris, 
                    file=file_data
                )
            discharge_epicris.save()
        return transferred_disease
