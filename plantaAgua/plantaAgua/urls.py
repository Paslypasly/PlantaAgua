from django.contrib import admin
from django.urls import path, include
from pedidos.views import dashboard_pedidos

urlpatterns = [
    path('', dashboard_pedidos, name='dashboard_pedidos'),
    path('admin/', admin.site.urls),
    path('api/', include('pedidos.api_urls')),
    path('', include('django.contrib.auth.urls')),
    path('web/', include('pedidos.web_urls')),
    path('web/calidad/', include('calidad.web_urls')),  # ✅ calidad
    # ❌ quita (o comenta) la línea que incluía clientes:
    # path('web/', include('clientes.web_urls')),
]
