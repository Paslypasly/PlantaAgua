# inventario/urls.py
from django.urls import path
from .views import (
    InsumoListView,
    MovimientoInventarioListView,
    MovimientoInventarioCreateView,
)

urlpatterns = [
    path("insumos/", InsumoListView.as_view(), name="inventario_insumos"),
    path("movimientos/", MovimientoInventarioListView.as_view(), name="inventario_movimientos"),
    path("movimientos/nuevo/", MovimientoInventarioCreateView.as_view(), name="inventario_movimiento_nuevo"),
]
