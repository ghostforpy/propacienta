from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

IS_DOCTOR_HEADER = "IsDoctor"
IS_DOCTOR_HEADER_STATUS = "true"


def request_by_doctor(request):
    if request.user != AnonymousUser:
        if IS_DOCTOR_HEADER in request.headers:
            if request.headers.get(IS_DOCTOR_HEADER) == IS_DOCTOR_HEADER_STATUS:
                if request.user.doctor != None:
                    if request.user.doctor.is_active:
                        return request.user.doctor
    return None


class RequestByDoctor(BasePermission):
    """
    Object-level permission to only allow requests by active doctors.
    """

    def has_permission(self, request, view):
        return request_by_doctor(request) is not None

    def has_object_permission(self, request, view, obj):
        # if request.user == obj.pacient.user:
        #    return True
        return request_by_doctor(request) is not None
