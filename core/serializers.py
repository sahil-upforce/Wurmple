from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    class Meta:
        fields = ("public_id",)
        read_only_fields = ("public_id",)
