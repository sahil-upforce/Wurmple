from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from core.mixins.views import CustomModelViewSet
from user_app import serializers
from user_app.models import Gender

User = get_user_model()


class GenderModelViewSet(CustomModelViewSet):
    serializer_class = serializers.GenderSerializer
    queryset = Gender.objects.all()


class UserModelViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CreateUserSerializer
        elif self.action == "update":
            return serializers.UpdateUserSerializer
        return super().get_serializer_class()
