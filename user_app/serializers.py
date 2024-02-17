from rest_framework import serializers

from core.mixins.serializers import BaseSerializer
from core.serializers import BaseNameCodeSerializer
from user_app.models import Gender


class GenderSerializer(BaseNameCodeSerializer, serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = (*BaseSerializer.Meta.fields, "name", "code")
        read_only_fields = (*BaseSerializer.Meta.read_only_fields,)
