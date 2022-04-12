from rest_framework.permissions import BasePermission

from doctors.utils import request_by_doctor


def analisis_result_dir(instance, filename: str) -> str:
    return "private/analisis_results/pacient_%s/%s" % (
        instance.analysis_result.pacient.id, filename
    )


def analisis_results_images_dir(instance, filename: str) -> str:
    return "private/analisis_results/images/pacient_%s/%s" % (
        instance.analysis_result.pacient.id, filename
    )


def analisis_results_files_dir(instance, filename: str) -> str:
    return "private/analisis_results/files/pacient_%s/%s" % (
        instance.analysis_result.pacient.id, filename
    )


class RequestByTreatingDoctor(BasePermission):
    """
    Object-level permission to only allow requests by active treating doctors.
    """
    # def has_permission(self, request, view):
    #     return request_by_doctor(request) is not None

    def has_object_permission(self, request, view, obj):
        doctor = request_by_doctor(request)
        if doctor is None:
            return False
        return doctor in obj.analysis_result.pacient.treating_doctors.all()


class IsOwnerOfAnalisObject(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """
    def has_permission(self, request, view):
        return request.user.pacient.id == view.kwargs.get('pacient_id')

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user == obj.analysis_result.pacient.user:
            return True
        return False


class RequestByTreatingDoctorAnalisResult(BasePermission):
    """
    Object-level permission to only allow requests by active treating doctors.
    """
    def has_permission(self, request, view):
        return request_by_doctor(request) is not None

    def has_object_permission(self, request, view, obj):
        doctor = request_by_doctor(request)
        if doctor is None:
            return False
        return doctor in obj.pacient.treating_doctors.all()


class IsOwnerOfAnalisResultObject(BasePermission):
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


class IsOwnerOfAnalisResultFileAndImageObject(BasePermission):
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


class RequestByTreatingDoctorAnalisResultFileAndImage(BasePermission):
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
