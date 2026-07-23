"""Rotas raiz do projeto King Street.

A loja pública e o painel administrativo são totalmente separados
(Arquitetura 01 e 05).
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from apps.core import views as core_views

urlpatterns = [
    # Loja pública
    path("", include("apps.store.urls")),
    # Painel administrativo (separado da loja)
    path("painel/", include("apps.dashboard.urls")),
    # PWA
    path("manifest.webmanifest", core_views.manifest, name="pwa-manifest"),
    path("service-worker.js", core_views.service_worker, name="pwa-service-worker"),
    path("offline/", core_views.offline, name="pwa-offline"),
]

handler404 = "apps.core.views.error_404"
handler500 = "apps.core.views.error_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
