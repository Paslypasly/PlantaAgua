# sensores/urls.py
from django.urls import path
from .views import (
    DashboardPlantaView,
    SensorListView,
    SensorDetailView,
    AlertaListView,
    AlertaDetailView,
    ReglaListView,
    ReglaCreateView,
    ReglaUpdateView,
    LecturasHistorialView,
    ActuadorListView,
    ActuadorDetailView,
)

urlpatterns = [
    # Dashboard general planta + IoT
    path("dashboard/", DashboardPlantaView.as_view(), name="dashboard_planta"),

    # Sensores
    path("sensores/", SensorListView.as_view(), name="sensores_list"),
    path("sensores/<int:pk>/", SensorDetailView.as_view(), name="sensor_detalle"),

    # Alertas
    path("alertas/", AlertaListView.as_view(), name="alertas_list"),
    path("alertas/<int:pk>/", AlertaDetailView.as_view(), name="alerta_detalle"),

    # Reglas de control (solo operario/admin)
    path("reglas/", ReglaListView.as_view(), name="reglas_list"),
    path("reglas/nueva/", ReglaCreateView.as_view(), name="regla_create"),
    path("reglas/<int:pk>/editar/", ReglaUpdateView.as_view(), name="regla_update"),

    # Historial de lecturas
    path("lecturas/", LecturasHistorialView.as_view(), name="lecturas_historial"),

    # Actuadores
    path("actuadores/", ActuadorListView.as_view(), name="actuadores_list"),
    path("actuadores/<int:pk>/", ActuadorDetailView.as_view(), name="actuador_detalle"),
]
