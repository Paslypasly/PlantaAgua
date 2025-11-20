# ventas/urls.py
from django.urls import path
from .views import PedidoListView, PedidoCreateView

urlpatterns = [
    path("pedidos/", PedidoListView.as_view(), name="ventas_pedidos"),
    path("pedidos/nuevo/", PedidoCreateView.as_view(), name="ventas_pedido_nuevo"),
]
