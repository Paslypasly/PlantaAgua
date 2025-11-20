# logistica/urls.py
from django.urls import path
from .views import RutaEntregaListView, RutaEntregaCreateView

urlpatterns = [
    path("rutas/", RutaEntregaListView.as_view(), name="logistica_rutas"),
    path("rutas/nueva/", RutaEntregaCreateView.as_view(), name="logistica_ruta_nueva"),
]
