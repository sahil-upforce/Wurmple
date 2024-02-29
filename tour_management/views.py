from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsSuperUser, IsTouristOrGuide
from tour_management.models import Place
from tour_management.serializers import CreateUpdatePlaceSerializer, PlaceSerializer


class PlaceModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (IsAuthenticated, IsTouristOrGuide)

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ("create", "update", "partial_update"):
            permission_classes = (IsAuthenticated, IsSuperUser)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return CreateUpdatePlaceSerializer
        return self.serializer_class
