from rest_framework.permissions import BasePermission

from doctors.utils import request_by_doctor


def discharge_epicrisis_dir(instance, filename: str) -> str:
    return "private/discharge_epicrisis/pacient_%s/%s" % (
        instance.discharge_epicris.pacient.id, filename
    )


def discharge_epicrisis_images_dir(instance, filename: str) -> str:
    return "private/discharge_epicrisis/images/pacient_%s/%s" % (
        instance.discharge_epicris.pacient.id, filename
    )


def discharge_epicrisis_files_dir(instance, filename: str) -> str:
    return "private/discharge_epicrisis/files/pacient_%s/%s" % (
        instance.discharge_epicris.pacient.id, filename
    )


class RequestByTreatingDoctorTransferredOrChronicDisease(BasePermission):
    """
    Object-level permission to only allow requests by active treating doctors.
    """
    def has_permission(self, request, view):
        pacient_id = view.kwargs.get('pacient_id')
        doctor = request_by_doctor(request)
        if doctor is not None:
            try:
                pacient = doctor.pacients.filter(id=int(pacient_id)).get()
                return pacient is not None
            except:
                pass
        return False

    def has_object_permission(self, request, view, obj):
        doctor = request_by_doctor(request)
        if doctor is None:
            return False
        return doctor in obj.pacient.treating_doctors.all()


class IsOwnerOfTransferredOrChronicDiseaseObject(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """
    def has_permission(self, request, view):
        return request.user.pacient.id == view.kwargs.get('pacient_id')

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user == obj.pacient.user:
            return True
        return False


class IsOwnerOfDischargeEpicrisImageOrFileObject(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """
    # def has_permission(self, request, view):
    #     return request.user.pacient.id == view.kwargs.get('pacient_id')

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user.pacient == obj.discharge_epicris.pacient:
            return True
        return False


class RequestByTreatingDoctorDischargeEpicrisImageOrFile(BasePermission):
    """
    Object-level permission to only allow requests by active treating doctors.
    """
    # def has_permission(self, request, view):
    #     pacient_id = view.kwargs.get('pacient_id')
    #     doctor = request_by_doctor(request)
    #     if doctor is not None:
    #         try:
    #             pacient = doctor.pacients.filter(id=int(pacient_id)).get()
    #             return pacient is not None
    #         except:
    #             pass
    #     return False

    def has_object_permission(self, request, view, obj):
        doctor = request_by_doctor(request)
        if doctor is None:
            return False
        return doctor in obj.discharge_epicris.pacient.treating_doctors.all()


class IsOwnerOfDischargeEpicrisImageAndFileObject(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """
    def has_permission(self, request, view):
        try:
            return request.user.pacient.id == int(request.headers.get("Pacientid", None))
        except:
            return False

    # def has_object_permission(self, request, view, obj):
    #     # Read permissions are allowed to any request,
    #     # so we'll always allow GET, HEAD or OPTIONS requests.
    #     # # Instance must have an attribute named `owner`.
    #     if request.user == obj.analysis_result.pacient.user:
    #         return True
    #     return False


class RequestByTreatingDoctorDischargeEpicrisImageAndFile(BasePermission):
    """
    Object-level permission to only allow requests by active treating doctors.
    """
    def has_permission(self, request, view):
        doctor = request_by_doctor(request)
        if doctor is not None:
            try:
                pacient = doctor.pacients.filter(
                    id=int(request.headers.get("Pacientid", None))
                ).get()
                return pacient is not None
            except:
                pass
        return False

    # def has_object_permission(self, request, view, obj):
    #     doctor = request_by_doctor(request)
    #     if doctor is None:
    #         return False
    #     return doctor in obj.analysis_result.pacient.treating_doctors
