from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import Group

from .models import Customer, Event, Contract


class IsSales(BasePermission):
    """"""

    message = "Only members of the sales team can access this."

    def has_permission(self, request, view):
        sales_group = Group.objects.get(name="sales")
        return sales_group in request.user.groups.iterator()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, (Customer, Contract)):
            return obj.sales_contact == request.user
        return False


class IsSupport(BasePermission):
    """"""

    message = "Only members of the support team can access this."

    def has_permission(self, request, view):
        support_group = Group.objects.get(name="support")
        return support_group in request.user.groups.iterator()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Event):
            return obj.support_contact == request.user
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return True


class IsAdmin(BasePermission):
    """"""

    message = "Only admins can access this."

    def has_permission(self, request, view):
        admin_group = Group.objects.get(name="admin")
        return admin_group in request.user.groups.iterator()

    def has_object_permission(self, request, view, obj):
        return True
