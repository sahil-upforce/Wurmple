from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.mixins.routers import NoSlashRouter
from user_app import views

app_name = "user_app"

user_router = NoSlashRouter()
user_router.register(r"accounts", views.UserModelViewSet, basename="accounts")
user_router.register(r"genders", views.GenderModelViewSet, basename="genders")

urlpatterns = [
    path("", include(user_router.urls)),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
