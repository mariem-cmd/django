
import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import DeviceSession

class AppUserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "full_name", "date_joined")

class DeviceSessionType(DjangoObjectType):
    is_expired = graphene.Boolean()

    class Meta:
        model = DeviceSession
        fields = ("id", "device_id", "token", "device_info", "created_at", "expiration_date", "is_expired")

    def resolve_is_expired(self, info):
        return self.is_expired()

