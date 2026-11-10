"""Project-wide middleware."""


class ContentSecurityPolicyMiddleware:
    """Add a conservative Content-Security-Policy header to every response.

    Inline scripts and styles are still allowed because the project uses them
    in templates; everything else is restricted to the site itself plus the
    CDNs that are explicitly used by the frontend.
    """

    POLICY = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://esm.run; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com "
        "https://cdn.jsdelivr.net; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https://www.gstatic.com https://cdn.jsdelivr.net; "
        "connect-src 'self'; "
        "worker-src 'self'; "
        "manifest-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers.setdefault("Content-Security-Policy", self.POLICY)
        return response
