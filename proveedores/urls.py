# proveedores/urls.py
from django.urls import path
from .views import ProveedorListView, ProveedorCreateView

urlpatterns = [
    path("", ProveedorListView.as_view(), name="proveedores_lista"),
    path("nuevo/", ProveedorCreateView.as_view(), name="proveedor_nuevo"),
]
