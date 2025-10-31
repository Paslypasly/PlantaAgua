from django.http import JsonResponse
from django.conf import settings

def require_api_key(view_func):
    def _wrapped(request, *args, **kwargs):
        key = request.headers.get("X-API-KEY") or request.META.get("HTTP_X_API_KEY")
        if not key or key != getattr(settings, "API_MOBILE_KEY", ""):
            return JsonResponse({"ok": False, "error": "unauthorized"}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped
