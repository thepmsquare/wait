from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .api_views import WeightEntryViewSet, UserSettingsView

router = DefaultRouter()
router.register(r"entries", WeightEntryViewSet, basename="weightentry")

urlpatterns = [
    path("", include(router.urls)),
    path("settings/", UserSettingsView.as_view(), name="api_user_settings"),
    path("auth/token/", obtain_auth_token, name="api_token_auth"),

    # OpenAPI Schema & API Documentation UI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
