from django.urls import path
from .views import ReporteResumenDiarioView

urlpatterns = [
    path("resumen-diario/", ReporteResumenDiarioView.as_view(), name="reporte_resumen_diario"),
]
