# planta/urls.py
from django.urls import path

from .views import EstadoEstanquesView, EventosPlantaView, ControlPlantaView

urlpatterns = [
    path("estanques/", EstadoEstanquesView.as_view(), name="estado_estanques"),
    path("eventos/", EventosPlantaView.as_view(), name="eventos_planta"),
    path("control/", ControlPlantaView.as_view(), name="control_planta"),
]
