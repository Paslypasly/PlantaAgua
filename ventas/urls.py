from django.urls import path

from .views import (
    PedidoListView,
    PedidoCreateView,
    CarritoView,
    CarritoAgregarView,
    CarritoEliminarView,
    CheckoutPublicoView,
)

app_name = "ventas"

urlpatterns = [
    # Panel interno
    path("pedidos/", PedidoListView.as_view(), name="ventas_pedidos"),
    path("pedidos/nuevo/", PedidoCreateView.as_view(), name="ventas_pedido_nuevo"),

    # Carrito + checkout públicos
    path("carrito/", CarritoView.as_view(), name="carrito"),
    path(
        "carrito/agregar/<int:producto_id>/",
        CarritoAgregarView.as_view(),
        name="carrito_agregar",
    ),
    path(
        "carrito/eliminar/<int:producto_id>/",
        CarritoEliminarView.as_view(),
        name="carrito_eliminar",
    ),
    path("checkout/", CheckoutPublicoView.as_view(), name="checkout_publico"),
]
