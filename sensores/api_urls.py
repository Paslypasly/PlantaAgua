# sensores/api_urls.py
from django.urls import path
from .api_views import (
    RegistrarLecturaAPIView,
    SensorDetailAPIView,
    SensorListAPIView,
    ReglaControlListCreateAPIView,
    RegistrarLecturaESP32APIView,
    SensoresDashboardAPIView,
)

urlpatterns = [
    # API “antigua” (si la sigues usando)
    path("lecturas/", RegistrarLecturaAPIView.as_view(), name="api_registrar_lectura"),
    path("sensores/", SensorListAPIView.as_view(), name="api_sensores_list"),
    path("sensores/<int:pk>/", SensorDetailAPIView.as_view(), name="api_sensores_detalle"),
    path("reglas/", ReglaControlListCreateAPIView.as_view(), name="api_reglas_listcreate"),

    # NUEVA API ESPECÍFICA PARA ESP32
    # /api/sensores/lectura/
    path("lectura/", RegistrarLecturaESP32APIView.as_view(), name="api_esp32_lectura"),

    # Mini-dashboard JSON
    # /api/sensores/dashboard/
    path("dashboard/", SensoresDashboardAPIView.as_view(), name="api_sensores_dashboard"),
]
