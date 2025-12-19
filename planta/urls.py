# planta/urls.py
from django.urls import path
from .views import (
    EstadoEstanquesView,
    ControlPlantaView,
    estado_estanques_api,
    inventario_set_selection_api,
)

urlpatterns = [
    path("estanques/", EstadoEstanquesView.as_view(), name="estado_estanques"),
    path("api/estado-estanques/", estado_estanques_api, name="estado_estanques_api"),

    # Inventario (modo + tipo)
    path("api/inventario/selection/", inventario_set_selection_api, name="inventario_set_selection_api"),

    path("control/", ControlPlantaView.as_view(), name="control_planta"),
]
