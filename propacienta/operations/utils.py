from rest_framework.permissions import BasePermission

from doctors.utils import request_by_doctor

# def transferred_operation_dir(instance, filename: str) -> str:
#     return "private/transferred_operation/pacient_%s/%s" % (
#         instance.transferred_operation.pacient.id,
#         filename,
#     )


def transferred_operation_images_dir(instance, filename: str) -> str:
    return "private/transferred_operation/images/pacient_%s/%s" % (
        instance.transferred_operation.pacient.id,
        filename,
    )


def transferred_operation_files_dir(instance, filename: str) -> str:
    return "private/transferred_operation/files/pacient_%s/%s" % (
        instance.transferred_operation.pacient.id,
        filename,
    )


class RequestByTreatingDoctorTransferredOperation(BasePermission):
    """
    Object-level permission to only allow requests by active treating doctors.
    """

    def has_permission(self, request, view):
        pacient_id = view.kwargs.get("pacient_id")
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


class IsOwnerOfTransferredOperationObject(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """

    def has_permission(self, request, view):
        return request.user.pacient.id == view.kwargs.get("pacient_id")

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user == obj.pacient.user:
            return True
        return False


class IsOwnerOfTransferredOperationImageOrFileObject(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """

    # def has_permission(self, request, view):
    #     return request.user.pacient.id == view.kwargs.get('pacient_id')

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user.pacient == obj.transferred_operation.pacient:
            return True
        return False


class RequestByTreatingDoctorTransferredOperationImageOrFile(BasePermission):
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
        return doctor in obj.transferred_operation.pacient.treating_doctors.all()


class IsOwnerOfTransferredOperationImageAndFileObject(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """

    def has_permission(self, request, view):
        try:
            return request.user.pacient.id == int(
                request.headers.get("Pacientid", None)
            )
        except:
            return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user == obj.transferred_operation.pacient.user:
            return True
        return False


class RequestByTreatingDoctorTransferredOperationImageAndFile(BasePermission):
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

    def has_object_permission(self, request, view, obj):
        doctor = request_by_doctor(request)
        if doctor is None:
            return False
        return doctor in obj.transferred_operation.pacient.treating_doctors.all()
