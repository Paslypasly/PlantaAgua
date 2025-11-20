# sensores/api_urls.py
from django.urls import path
from .api_views import RegistrarLecturaAPIView, SensorDetailAPIView, SensorListAPIView, ReglaControlListCreateAPIView

urlpatterns = [
    path("lecturas/", RegistrarLecturaAPIView.as_view(), name="api_registrar_lectura"),
    path("sensores/", SensorListAPIView.as_view(), name="api_sensores_list"),
    path("sensores/<int:pk>/", SensorDetailAPIView.as_view(), name="api_sensores_detalle"),
    path("reglas/", ReglaControlListCreateAPIView.as_view(), name="api_reglas_listcreate"),
]
