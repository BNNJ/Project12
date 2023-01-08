from django.db.models import Q
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .models import Customer, Contract, ContractStatus, Event, EventStatus
from .serializers import (
    UserSerializer,
    GroupSerializer,
    CustomerSerializer,
    ContractSerializer,
    ContractStatusSerializer,
    EventSerializer,
    EventStatusSerializer,
)
from .permissions import IsAdmin, IsSales, IsSupport, ReadOnly


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in "create":
            self.permission_classes = []
        # elif self.action in 'update':
        # 	self.permission_classes = [IsSelf | IsAdmin]
        return super().get_permissions()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAdmin]


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["first_name", "last_name", "email"]
    # permission_classes = [IsSales | IsAdmin]

    def get_queryset(self):
        user = self.request.user
        queryset = Customer.objects.all()
        admin_group = Group.objects.get(name="admin")
        if admin_group in user.groups.iterator():
            return queryset
        return queryset.filter(Q(sales_contact=user) | Q(events__support_contact=user))

    def perform_create(self, serializer):
        contact_id = self.request.data.get("sales_contact", self.request.user.id)
        contact = User.objects.get(id=contact_id)
        sales_group = Group.objects.get(name="sales")
        if sales_group in contact.groups.iterator():
            serializer.save(sales_contact=contact)
        else:
            raise APIException("Provided sales contact not in sales group")

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            self.permission_classes = [IsSales | IsSupport | IsAdmin]
        elif self.action == "destroy":
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [IsAdmin | IsSales]
        return super().get_permissions()


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "customer__first_name",
        "customer__last_name",
        "customer__email",
        "amount",
        "date_created",
    ]

    def get_queryset(self):
        user = self.request.user
        admin_group = Group.objects.get(name="admin")
        if admin_group in user.groups.iterator():
            return Contract.objects.all()
        return user.contracts.all()

    def get_permissions(self):
        if self.action in ["list", "update", "create"]:
            self.permission_classes = [IsAdmin | IsSales]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "customer__first_name",
        "customer__last_name",
        "customer__email",
        "date",
    ]

    def get_queryset(self):
        user = self.request.user
        admin_group = Group.objects.get(name="admin")
        if admin_group in user.groups.iterator():
            return Event.objects.all()
        return user.events.all() | Event.objects.filter(customer__sales_contact=user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAdmin | IsSales]
        elif self.action == "destroy":
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [IsAdmin | IsSupport]
        return super().get_permissions()


class ContractStatusViewSet(viewsets.ModelViewSet):
    serializer_class = ContractStatusSerializer
    queryset = ContractStatus.objects.all()
    permission_classes = [IsAdmin | (IsAuthenticated & ReadOnly)]


class EventStatusViewSet(viewsets.ModelViewSet):
    serializer_class = EventStatusSerializer
    queryset = EventStatus.objects.all()
    permission_classes = [IsAdmin | (IsAuthenticated & ReadOnly)]
