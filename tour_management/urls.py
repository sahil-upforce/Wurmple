from django.urls import include, path

from core.mixins.routers import NoSlashRouter
from tour_management import views

app_name = "tour_management"

tour_management_router = NoSlashRouter()
tour_management_router.register(r"places", views.PlaceModelViewSet, basename="places")

urlpatterns = [
    path("", include(tour_management_router.urls)),
]
