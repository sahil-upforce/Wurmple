from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers

from core.mixins.serializers import BaseSerializer
from core.models import Category, Language
from core.serializers import (
    BaseNameCodeSerializer,
    CategorySerializer,
    LanguageSerializer,
)
from user_app.models import Gender, SpokenLanguage, TourCategory

User = get_user_model()


class GenderSerializer(BaseNameCodeSerializer, serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = (*BaseSerializer.Meta.fields, "name", "code")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)


class SpokenLanguageSerializer(BaseSerializer):
    language = LanguageSerializer()

    class Meta:
        model = SpokenLanguage
        fields = (*BaseSerializer.Meta.fields, "language", "fluency")
        read_only_fields = (*BaseSerializer.Meta.fields,)


class TourCategorySerializer(BaseSerializer):
    category = CategorySerializer()

    class Meta:
        model = TourCategory
        fields = (*BaseSerializer.Meta.fields, "category_id")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)


class UserSerializer(BaseSerializer, serializers.ModelSerializer):
    gender = GenderSerializer(read_only=True)
    tour_categories = TourCategorySerializer(many=True, source="categories")
    spoken_languages = SpokenLanguageSerializer(many=True, source="languages")
    user_type_name = serializers.SerializerMethodField()

    @staticmethod
    def get_user_type_name(obj):
        return dict(User.USER_TYPE_CHOICES).get(obj.user_type)

    class Meta:
        model = User
        fields = (
            *BaseSerializer.Meta.fields,
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "address",
            "bio",
            "profile_picture",
            "is_available",
            "experience",
            "user_type_name",
            "gender",
            "spoken_languages",
            "tour_categories",
        )
        read_only_fields = (*BaseSerializer.Meta.fields, "user_type_name")
        extra_kwargs = {i: {"required": True} for i in fields}


class CreateUserSerializer(UserSerializer):
    gender = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all(), required=True)
    tour_categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    spoken_languages = serializers.PrimaryKeyRelatedField(many=True, queryset=Language.objects.all())
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            *BaseSerializer.Meta.fields,
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone",
            "user_type",
            "birth_date",
            "address",
            "bio",
            "profile_picture",
            "user_type_name",
            "gender",
            "experience",
            "tour_categories",
            "spoken_languages",
        )
        read_only_fields = (*BaseSerializer.Meta.fields, "user_type_name")
        extra_kwargs = {
            i: {"required": True}
            for i in [
                "username",
                "password",
                "first_name",
                "last_name",
                "email",
                "phone",
                "user_type",
                "gender",
                "tour_categories",
                "spoken_languages",
            ]
        }

    def validate_user_type(self, value):
        if value == User.USER_TYPE_GUIDE and not self.initial_data.get("experience"):
            raise serializers.ValidationError(f"Experience is required for {User.USER_TYPE_TOURIST_NAME} type user")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            languages = validated_data.pop("languages")
            tour_categories = validated_data.pop("tour_categories")
            validated_data["password"] = make_password(validated_data["password"])
            user = User.objects.create_user(**validated_data)
            SpokenLanguage.objects.bulk_create([SpokenLanguage(user=user, language=language) for language in languages])
            TourCategory.objects.bulk_create(
                [TourCategory(user=user, category=category) for category in tour_categories]
            )
        return user


class UpdateUserSerializer(UserSerializer):
    gender = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all(), required=True)
    tour_categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    spoken_languages = serializers.PrimaryKeyRelatedField(many=True, queryset=Language.objects.all())

    class Meta:
        model = User
        fields = (
            *BaseSerializer.Meta.fields,
            "username",
            "first_name",
            "last_name",
            "birth_date",
            "address",
            "bio",
            "profile_picture",
            "is_available",
            "experience",
            "user_type",
            "gender",
            "tour_categories",
            "spoken_languages",
        )
        read_only_fields = (*BaseSerializer.Meta.fields,)
        extra_kwargs = {
            i: {"required": True}
            for i in [
                "username",
                "first_name",
                "last_name",
                "user_type",
                "gender",
                "tour_categories",
                "spoken_languages",
            ]
        }

    def validate_user_type(self, value):
        if value == User.USER_TYPE_GUIDE and not self.initial_data.get("experience"):
            raise serializers.ValidationError(f"Experience is required for {User.USER_TYPE_TOURIST_NAME} type user")
        return value
