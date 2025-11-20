# produccion/urls.py
from django.urls import path

from .views import (
    PlanProduccionDiariaView,
    OrdenesProduccionListView,
    OrdenProduccionDetalleView,
    ConsumoInsumosView,
)

urlpatterns = [
    path(
        "plan-diario/",
        PlanProduccionDiariaView.as_view(),
        name="plan_produccion_diaria",
    ),
    path(
        "ordenes/",
        OrdenesProduccionListView.as_view(),
        name="ordenes_produccion_list",
    ),
    path(
        "orden/<int:pk>/",
        OrdenProduccionDetalleView.as_view(),
        name="orden_produccion_detalle",
    ),
    path(
        "consumo-insumos/",
        ConsumoInsumosView.as_view(),
        name="consumo_insumos",
    ),
]
