# cuentas/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PanelAdminView,
    PanelOperarioView,
    PanelConductorView,
    PanelGerenteView,
    UsuarioListView,
    UsuarioCreateView,
    UsuarioUpdateView,
    UsuarioDeleteView,
    PerfilView,  
)

urlpatterns = [
    # auth estándar
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # perfil propio
    path("perfil/", PerfilView.as_view(), name="perfil"),

    # paneles por rol
    path("panel/admin/",     PanelAdminView.as_view(), name="panel_admin"),
    path("panel/operario/",  PanelOperarioView.as_view(), name="panel_operario"),
    path("panel/conductor/", PanelConductorView.as_view(), name="panel_conductor"),
    path("panel/gerente/",   PanelGerenteView.as_view(), name="panel_gerente"),

    # gestión de usuarios (solo ADMIN)
    path("usuarios/",                 UsuarioListView.as_view(),   name="usuarios_list"),
    path("usuarios/nuevo/",           UsuarioCreateView.as_view(), name="usuario_create"),
    path("usuarios/<int:pk>/editar/", UsuarioUpdateView.as_view(), name="usuario_update"),
    path("usuarios/<int:pk>/eliminar/", UsuarioDeleteView.as_view(), name="usuario_delete"),
]
