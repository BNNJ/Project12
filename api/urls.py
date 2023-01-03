from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    UserViewSet,
    CustomerViewSet,
    ContractViewSet,
    EventViewSet,
    ContractStatusViewSet,
    EventStatusViewSet,
    GroupViewSet,
)

router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="user")
router.register("groups", GroupViewSet, basename="group")
router.register("customers", CustomerViewSet, basename="customer")
router.register("contracts", ContractViewSet, basename="contract")
router.register("events", EventViewSet, basename="event")
router.register("event_status", EventStatusViewSet, basename="event_status")
router.register("contract_status", ContractStatusViewSet, basename="contract_status")

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("signup/", UserViewSet.as_view({"post": "create"}), name="signup"),
    *router.urls,
]
