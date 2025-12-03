from django.urls import path
from .views import CatalogoPublicoView, ProductoDetallePublicoView

app_name = "productos"

urlpatterns = [
    path("catalogo/", CatalogoPublicoView.as_view(), name="catalogo_publico"),
    path("detalle/<int:pk>/", ProductoDetallePublicoView.as_view(), name="detalle_publico"),
]
