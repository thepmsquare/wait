"""Project-level views."""

from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound


def service_worker(request: HttpRequest) -> HttpResponse:
    """Serve the service worker from the site root.

    Registering ``/static/sw.js`` would limit the worker's scope to
    ``/static/``, so the file is served from ``/sw.js`` instead.
    """

    path = finders.find("sw.js")
    if not path:
        fallback = Path(settings.STATIC_ROOT) / "sw.js"
        if fallback.exists():
            path = str(fallback)
    if not path:
        return HttpResponseNotFound("service worker not found")

    with open(path, "rb") as worker_file:
        content = worker_file.read()

    response = HttpResponse(content, content_type="application/javascript")
    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache"
    return response
