from django.urls import include, path

from core import views
from core.mixins.routers import NoSlashRouter

app_name = "core"

core_router = NoSlashRouter()
core_router.register(r"countries", views.CountryModelViewSet, "countries")
core_router.register(r"states", views.StateModelViewSet, "states")
core_router.register(r"cities", views.CityModelViewSet, "cities")
core_router.register(r"languages", views.LanguageModelViewSet, "languages")
core_router.register(r"categories", views.CategoryModelViewSet, "categories")

urlpatterns = [
    path("", include(core_router.urls)),
]
