"""
Attaches `request.organization` from the authenticated user so views
and viewsets can scope querysets without repeating lookup logic.

Note: this runs after AuthenticationMiddleware in MIDDLEWARE, but since
DRF's JWTAuthentication runs at the view layer (not Django's session
auth), `request.user` may not be populated yet here for JWT-authenticated
API calls. Viewsets should still call `request.user.organization`
directly - this middleware is a convenience for Django-session-based
views (e.g. the admin) and future HTMX server-rendered views.
"""


class TenantContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        request.organization = None
        if user is not None and getattr(user, "is_authenticated", False):
            request.organization = getattr(user, "organization", None)
        return self.get_response(request)
