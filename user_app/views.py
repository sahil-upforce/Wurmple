from core.mixins.views import CustomModelViewSet
from user_app import serializers
from user_app.models import Gender


class GenderModelViewSet(CustomModelViewSet):
    serializer_class = serializers.GenderSerializer
    queryset = Gender.objects.all()
