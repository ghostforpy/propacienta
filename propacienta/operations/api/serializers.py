from rest_framework import serializers

from ..models import (
    Operation,
    TransferredOperation,
    TransferredOperationFile,
    TransferredOperationImage,
)


class ValidatePacientIdMixin:
    def validate_pacient(self, value):
        pacient_id = self.context["view"].kwargs["pacient_id"]
        if value.id != pacient_id:
            raise serializers.ValidationError("Wrong pacientId.")
        return value


class OperationSerializer(serializers.ModelSerializer):
    operation_count = serializers.IntegerField(default=0)

    class Meta:
        model = Operation
        fields = "__all__"


class TransferredOperationFileSerializer(serializers.ModelSerializer):
    """Сериалайзер для файлов выписных эпикризов перенесенных операций."""

    file = serializers.CharField(source="file.url")
    delete_url = serializers.CharField(source="get_absolute_url")

    class Meta:
        model = TransferredOperationFile
        exclude = ["transferred_operation", "id"]


class TransferredOperationImageSerializer(serializers.ModelSerializer):
    """Сериалайзер для изображений выписных эпикризов перенесенных операций."""

    image = serializers.CharField(source="image.url")
    delete_url = serializers.CharField(source="get_absolute_url")

    class Meta:
        model = TransferredOperationImage
        exclude = ["transferred_operation", "id"]


class TransferredOperationSerializer(
    ValidatePacientIdMixin, serializers.ModelSerializer
):
    transferred_operation_files = TransferredOperationFileSerializer(
        many=True, required=False
    )
    transferred_operation_images = TransferredOperationImageSerializer(
        many=True, required=False
    )
    operation_title = serializers.CharField(read_only=True, source="operation.title")

    class Meta:
        model = TransferredOperation
        fields = "__all__"

    def create(self, validated_data):
        images_data = self.context["request"].data.getlist("images")
        files_data = self.context["request"].data.getlist("files")
        transferred_operation = TransferredOperation.objects.create(**validated_data)

        # if instance.images.count() + len(images_data) > MAXIMUM_SERVICES_IMAGES_COUNT:
        #     raise ValidationError(
        #         "Maximum count of images is {}".format(MAXIMUM_SERVICES_IMAGES_COUNT)
        #     )
        for image_data in images_data:
            # сохранянем изображения
            TransferredOperationImage.objects.create(
                transferred_operation=transferred_operation, image=image_data
            )
        for file_data in files_data:
            # сохранянем файлы
            TransferredOperationFile.objects.create(
                transferred_operation=transferred_operation, file=file_data
            )
        transferred_operation.save()
        return transferred_operation
