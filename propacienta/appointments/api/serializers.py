from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from hospitals.models import DEFAULT_HOSPITAL
from work_schedules.models import NotWorkingPeriod, WorkDay

from ..models import AppointmentOrder, AppointmentSurvey


class AppointmentOrderSerializer(serializers.ModelSerializer):
    hospital = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=DEFAULT_HOSPITAL
    )

    class Meta:
        model = AppointmentOrder
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                # у доктора не может быть двух записей на одно и то же время
                queryset=AppointmentOrder.objects.all(),
                fields=['doctor', 'dt']
            ),
            UniqueTogetherValidator(
                # у пациента не может быть двух записей на одно и то же время
                queryset=AppointmentOrder.objects.all(),
                fields=['pacient', 'dt']
            )
        ]

    # def create(self, validated_data):
    #     return super().create(validated_data)

    def validate(self, data):
        doctor = data["doctor"]
        try:
            doctor_specialization = data["doctor_specialization"]
            #  check doctor_specialization
            if doctor_specialization not in doctor.specializations.all():
                raise serializers.ValidationError("Wrong doctor_specialization.")
        except KeyError:
            pass
        try:
            doctor_sub_specialization = data["doctor_sub_specialization"]
            #  check doctor_sub_specialization
            if doctor_sub_specialization not in doctor.sub_specialization.all():
                raise serializers.ValidationError("Wrong doctor_sub_specialization.")
        except KeyError:
            pass
        # hospital = data["hospital"]
        dt = data["dt"]
        try:
            # выбираем рабочий период
            w = WorkDay.objects.filter(
                doctor=doctor,
                hospital=DEFAULT_HOSPITAL,  # default hospital
                date=dt.date(),
                since__lte=dt.time(),  # проверить
                to__gt=dt.time(),  # проверить
            ).get()
            # проверяем нет ли нерабочих периодов на эту дату
            if NotWorkingPeriod.objects.filter(
                doctor=doctor,
                hospital=DEFAULT_HOSPITAL,  # default hospital
                since__gte=dt.date(),
                is_open=True
            ).filter(Q(to__lt=dt.date()) | Q(to__isnull=True)).exists():
                raise serializers.ValidationError("Not work period for this doctor.")
        except WorkDay.MultipleObjectsReturned:
            # внутренняя ошибка (в расписании доктора есть пересекающиеся рабочие периоды)
            raise serializers.ValidationError("WorkDay MultipleObjectsReturned.")
        except WorkDay.DoesNotExist:
            # нет рабочего периода
            raise serializers.ValidationError("WorkDay DoesNotExist.")
        if w.reserve_timeslot(dt.time()):
            data["end"] = dt + timedelta(minutes=w.appointment_duration)
            return data
        else:
            # выбранное время занято или не соответствует сетке приемов
            raise serializers.ValidationError("Timeslot is busy.")


class AppointmentOrderPacientSerializer(AppointmentOrderSerializer):
    name = serializers.CharField(source="get_doctor_name", read_only=True)

    def validate_pacient(self, value):
        pacient_id = self.context["request"].user.pacient.id
        if value.id != pacient_id:
            raise serializers.ValidationError("Wrong pacientId.")
        return value


class AppointmentOrderDoctorSerializer(AppointmentOrderSerializer):
    name = serializers.CharField(source="get_pacient_name", read_only=True)
    # start = serializers.DateTimeField(source="dt", read_only=True)

    def validate_doctor(self, value):
        doctor_id = self.context["request"].user.doctor.id
        if value.id != doctor_id:
            raise serializers.ValidationError("Wrong doctorId.")
        return value


class AppointmentSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSurvey
        fields = "__all__"


# class AnalysisResultSerializer(ValidatePacientIdMixin, serializers.ModelSerializer):
#     analysis_files = AnalysisResultsFileSerializer(many=True, required=False)
#     analysis_images = AnalysisResultsImageSerializer(many=True, required=False)

#     class Meta:
#         model = AnalysisResult
#         fields = "__all__"

#     def create(self, validated_data):
#         images_data = self.context["request"].data.getlist("images")
#         files_data = self.context["request"].data.getlist("files")
#         analysis_result = AnalysisResult.objects.create(**validated_data)
#         # if instance.images.count() + len(images_data) > MAXIMUM_SERVICES_IMAGES_COUNT:
#         #     raise ValidationError(
#         #         "Maximum count of images is {}".format(MAXIMUM_SERVICES_IMAGES_COUNT)
#         #     )
#         for image_data in images_data:
#             # сохранянем изображения
#             AnalysisResultsImage.objects.create(
#                 analysis_result=analysis_result, image=image_data
#             )
#         for file_data in files_data:
#             # сохранянем файлы
#             AnalysisResultsFile.objects.create(
#                 analysis_result=analysis_result, file=file_data
#             )
#         analysis_result.save()
#         return analysis_result
