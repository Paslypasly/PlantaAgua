from django.urls import path
from .views import (
    PanelAdminView,
    PanelOperarioView,
    PanelConductorView,
    PanelGerenteView,
    redirigir_por_rol,
)

urlpatterns = [
    path("panel/admin/",     PanelAdminView.as_view(),     name="panel_admin"),
    path("panel/operario/",  PanelOperarioView.as_view(),  name="panel_operario"),
    path("panel/conductor/", PanelConductorView.as_view(), name="panel_conductor"),
    path("panel/gerente/",   PanelGerenteView.as_view(),   name="panel_gerente"),
    path("panel/",           redirigir_por_rol,            name="panel_por_rol"),
]
