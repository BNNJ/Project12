from rest_framework.filters import BaseFilterBackend

from .views import CustomerViewSet, EventViewSet


class UserIsSalesContact(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(sales_contact=request.user)


class UserIsSupportContact(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if isinstance(view, EventViewSet):
            return queryset.filter(support_contact=request.user)
        elif isinstance(view, CustomerViewSet):
            return queryset.filter(support_contact=request.user)
