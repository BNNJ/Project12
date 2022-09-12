from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Group, User, Customer, Event, Contract

groups = Group.objects.all()
sales_group = next(g for g in groups if g.name == "sales")
support_group = next(g for g in groups if g.name == "support")
admin_group = next(g for g in groups if g.name == "admin")


class IsSales(BasePermission):
	""""""
	message = "Only members of the sales team can access this."

	def has_permission(self, request, view):
		return sales_group in request.user.groups.iterator()

	def has_object_permission(self, request, view, obj):
		if isinstance(obj, (Customer, Contract)):
			return obj.sales_contact == request.user
		return False


class IsSupport(BasePermission):
	""""""
	message = "Only members of the support team can access this."

	def has_permission(self, request, view):
		return support_group in request.user.groups.iterator()

	def has_object_permission(self, request, view, obj):
		if isinstance(obj, Event):
			return obj.support_contact == user
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
		return admin_group in request.user.groups.iterator()

	def has_object_permission(self, request, view, obj):
		return True
