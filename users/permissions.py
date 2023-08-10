from rest_framework.permissions import BasePermission


class IsProvider(BasePermission):
    message = "Unauthorized access, Only users of type PROVIDER can access."

    def has_permission(self, request, view):
        user = request.user
        if user.user_type == "PROVIDER":
            return True
        else:
            return False


class IsCustomer(BasePermission):
    message = "Unauthorized access, Only users of type CUSTOMER can access."

    def has_permission(self, request, view):
        user = request.user
        if user.user_type == "CUSTOMER":
            return True
        else:
            return False


class IsBanker(BasePermission):
    message = "Unauthorized access, Only users of type BANKER can access."

    def has_permission(self, request, view):
        user = request.user
        if user.user_type == "BANKER":
            return True
        else:
            return False
