from core.mixins.routers import NoSlashRouter
from user_app import views

app_name = "user_app"

user_router = NoSlashRouter()
user_router.register(r"accounts", views.UserModelViewSet, basename="accounts")
user_router.register(r"genders", views.GenderModelViewSet, basename="genders")
