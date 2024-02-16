from django.contrib import admin

from core.models import BaseModel, Category, City, Country, Language, State


class BaseAdmin(admin.ModelAdmin):
    exclude = tuple(field.name for field in BaseModel._meta.fields)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Country)
class CountryAdmin(BaseAdmin):
    pass


@admin.register(State)
class StateAdmin(BaseAdmin):
    pass


@admin.register(City)
class CityAdmin(BaseAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(BaseAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    pass
