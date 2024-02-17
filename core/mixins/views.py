from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class CustomModelViewSet(ModelViewSet):
    def get_message(self, instance):
        return f"The record with public_id {instance.pk} has been deleted."

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = self.get_message(instance)
        return Response({"detail": message}, status=status.HTTP_200_OK)
