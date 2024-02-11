from django.contrib import admin

from core.models import BaseModel


class BaseAdmin(admin.ModelAdmin):
    exclude = tuple(field.name for field in BaseModel._meta.fields)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
