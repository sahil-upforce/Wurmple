from django.db.models import Q
from rest_framework import serializers

from core.mixins.serializers import BaseSerializer
from core.models import Category, City, Country, Language, State


class BaseNameCodeSerializer(BaseSerializer):
    name = serializers.CharField(max_length=255, required=True)
    code = serializers.CharField(max_length=15, required=True)

    def validate_code(self, value):
        filters = Q(code=value.upper())
        if self.instance:
            filters &= ~Q(pk=self.instance.pk)
        if self.Meta.model.objects.filter(filters).exists():
            raise serializers.ValidationError(
                detail=f"{self.Meta.model._meta.model_name} code already exists".capitalize()
            )
        return value


class CountrySerializer(BaseNameCodeSerializer, serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (*BaseSerializer.Meta.fields, "name", "code")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)


class StateSerializer(BaseNameCodeSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        fields = (*BaseSerializer.Meta.fields, "name", "code", "country")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)


class StateCreateSerializer(StateSerializer, serializers.ModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=True)

    class Meta:
        model = State
        fields = (*BaseSerializer.Meta.fields, "name", "code", "country_id")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)

    def validate_country_id(self, value):
        return value.pk


class CitySerializer(BaseNameCodeSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = City
        fields = (*BaseSerializer.Meta.fields, "name", "code", "state")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)


class CityCreateSerializer(StateSerializer, serializers.ModelSerializer):
    state_id = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), required=True)

    class Meta:
        model = City
        fields = (*BaseSerializer.Meta.fields, "name", "code", "state_id")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)

    def validate_state_id(self, value):
        return value.pk


class LanguageSerializer(BaseNameCodeSerializer, serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (*BaseSerializer.Meta.fields, "name", "code")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)


class CategorySerializer(BaseNameCodeSerializer, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (*BaseSerializer.Meta.fields, "name", "code")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)
