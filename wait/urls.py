"""URL configuration for wait project."""

from django.contrib import admin
from django.urls import include, path

from wait.views import service_worker

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sw.js", service_worker, name="service_worker"),
    path("", include("tracker.urls")),
    path("api/", include("tracker.api_urls")),
    path("accounts/", include("allauth.urls")),
]
