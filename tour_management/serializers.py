from django.db.models import Q
from rest_framework import serializers

from core.mixins.serializers import BaseSerializer
from core.models import Category, City
from core.serializers import CategorySerializer, CitySerializer
from tour_management.models import Place, PlaceCategory, PlaceImage


class PlaceCategorySerializer(BaseSerializer):
    category = CategorySerializer()

    class Meta:
        model = PlaceCategory
        fields = (*BaseSerializer.Meta.fields, "category_id")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)


class PlaceImageSerializer(BaseSerializer, serializers.ModelSerializer):
    uploaded_by = serializers.UUIDField(source="created_by.public_id")

    class Meta:
        model = PlaceImage
        fields = (*BaseSerializer.Meta.fields, "uploaded_by", "image")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)


class PlaceSerializer(BaseSerializer, serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    place_categories = PlaceCategorySerializer(many=True, source="categories_of_places")

    class Meta:
        model = Place
        fields = (
            *BaseSerializer.Meta.fields,
            "name",
            "code",
            "slug",
            "address",
            "description",
            "visiting_fees",
            "website",
            "latitude",
            "longitude",
            "city",
            "place_categories",
        )
        read_only_fields = (*BaseSerializer.Meta.fields,)

    def validate(self, data):
        latitude, longitude = data["latitude"], data["longitude"]
        filters = Q(latitude=latitude, longitude=longitude)
        if self.instance:
            filters &= ~Q(pk=self.instance.pk)
        if Place.objects.filter(filters).exists():
            raise serializers.ValidationError(
                detail=f"{self.Meta.model._meta.model_name} already exists with given latitude and longitude".capitalize()
            )
        return data

    def validate_code(self, value):
        filters = Q(code=value.upper())
        if self.instance:
            filters &= ~Q(pk=self.instance.pk)
        if self.Meta.model.objects.filter(filters).exists():
            raise serializers.ValidationError(
                detail=f"{self.Meta.model._meta.model_name} code already exists".capitalize()
            )
        return value


class CreateUpdatePlaceSerializer(PlaceSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=True)
    place_categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Place
        fields = (
            *BaseSerializer.Meta.fields,
            "name",
            "code",
            "slug",
            "address",
            "description",
            "visiting_fees",
            "website",
            "latitude",
            "longitude",
            "city",
            "place_categories",
        )
        read_only_fields = (*BaseSerializer.Meta.fields, "slug")
        extra_kwargs = {
            i: {"required": True}
            for i in [
                "name",
                "code",
                "address",
                "description",
                "latitude",
                "longitude",
                "city",
                "place_categories",
            ]
        }
