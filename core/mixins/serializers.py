from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    public_id = serializers.UUIDField(read_only=True)

    class Meta:
        fields = ("public_id",)
        read_only_fields = ("public_id",)
