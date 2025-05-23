from rest_framework.permissions import IsAuthenticated

from core import serializers
from core.mixins.views import CustomModelViewSet
from core.models import Category, City, Country, Language, State
from core.permissions import IsSuperUser


class CountryModelViewSet(CustomModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = serializers.CountrySerializer
    queryset = Country.objects.all()


class StateModelViewSet(CustomModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = serializers.StateSerializer
    queryset = State.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return serializers.StateCreateSerializer
        return super().get_serializer_class()


class CityModelViewSet(CustomModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = serializers.CitySerializer
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return serializers.CityCreateSerializer
        return super().get_serializer_class()


class LanguageModelViewSet(CustomModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = serializers.LanguageSerializer
    queryset = Language.objects.all()


class CategoryModelViewSet(CustomModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
