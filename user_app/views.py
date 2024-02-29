from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.mixins.views import CustomModelViewSet
from core.permissions import IsObjectOwnerOrSuperUser, IsSuperUser
from user_app import serializers
from user_app.models import Gender

User = get_user_model()


class GenderModelViewSet(CustomModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = serializers.GenderSerializer
    queryset = Gender.objects.all()


class UserModelViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated, IsObjectOwnerOrSuperUser)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CreateUserSerializer
        elif self.action == "update":
            return serializers.UpdateUserSerializer
        return super().get_serializer_class()
