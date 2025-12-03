from django.contrib import admin
from django.urls import path, include
from pages.views import HomeView  

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),  
    path("api/iot/", include("sensores.api_urls")),
    path("api/sensores/", include("sensores.api_urls")),
    path("planta/", include("planta.urls")),
    path("cuentas/", include("cuentas.urls")),
    path("pages/", include("pages.urls")),
    path("inventario/", include("inventario.urls")),
    path("proveedores/", include("proveedores.urls")),
    path("compras/", include("compras.urls")),
    path("clientes/", include("clientes.urls")),
    path("ventas/", include("ventas.urls")),
    path("logistica/", include("logistica.urls")),
    path("reportes/", include("reportes.urls")),
    path("produccion/", include("produccion.urls")),
    path("productos/", include("productos.urls")),
]

handler403 = "core.views.error_403_view"
handler404 = "core.views.error_404_view"
handler500 = "core.views.error_500_view"
