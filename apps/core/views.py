from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.decorators.http import require_GET


@require_GET
def manifest(request):
    """Manifesto do PWA (Arquitetura 05)."""
    data = {
        "name": settings.STORE_NAME,
        "short_name": settings.STORE_NAME,
        "description": f"Catálogo e painel — {settings.STORE_NAME}",
        "start_url": "/painel/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#000000",
        "theme_color": "#000000",
        "icons": [
            {"src": static("pwa/icon-192.png"), "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": static("pwa/icon-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }
    return JsonResponse(data)


@require_GET
def service_worker(request):
    """Service worker do PWA, servido a partir da raiz para escopo total."""
    response = render(request, "pwa/service-worker.js", content_type="application/javascript")
    response["Service-Worker-Allowed"] = "/"
    return response


def offline(request):
    return render(request, "pwa/offline.html")


def error_404(request, exception=None):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)
