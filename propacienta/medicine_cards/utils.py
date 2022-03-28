from doctors.utils import request_by_doctor
from rest_framework.permissions import BasePermission

def analisis_result_dir(instance, filename: str) -> str:
    return "private/analisis_results/pacient_%s/%s" % (instance.analysis_result.pacient.id, filename)


class RequestByTreatingDoctorMedicineCard(BasePermission):
    """
    Object-level permission to only allow requests by active treating doctors.
    """
    def has_permission(self, request, view):
        return request_by_doctor(request) is not None

    def has_object_permission(self, request, view, obj):
        doctor = request_by_doctor(request)
        if doctor is None:
            return False
        return doctor in obj.pacient.treating_doctors


class RequestByTreatingDoctorResultIndependentResearch(BasePermission):
    """
    Object-level permission to only allow requests by active treating doctors.
    """
    def has_permission(self, request, view):
        return request_by_doctor(request) is not None

    def has_object_permission(self, request, view, obj):
        doctor = request_by_doctor(request)
        if doctor is None:
            return False
        return doctor in obj.medicine_card.pacient.treating_doctors


class IsOwnerOfMedicineCardObject(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user == obj.pacient.user:
            return True
        return False


class IsOwnerOfResultIndependentResearchObjects(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """
    def has_permission(self, request, view):
        #print('has perm', view, view.args, view.kwargs)
        return request.user.pacient.id == view.kwargs.get('pacient_id')
        #return request_by_doctor(request) is not None

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user == obj.medicine_card.pacient.user:
            return True
        return False