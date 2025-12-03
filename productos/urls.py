# productos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(
        "catalogo/",
        views.CatalogoPublicoView.as_view(),
        name="catalogo_publico",
    ),
    path(
        "catalogo/<int:pk>/",
        views.ProductoDetallePublicoView.as_view(),
        name="detalle_producto_publico",
    ),
]
