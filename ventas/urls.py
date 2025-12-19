# ventas/urls.py
from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    # carrito público
    path("carrito/", views.CarritoView.as_view(), name="carrito"),
    path("carrito/agregar/<int:producto_id>/", views.CarritoAgregarView.as_view(), name="carrito_agregar"),
    path("carrito/eliminar/<int:producto_id>/", views.CarritoEliminarView.as_view(), name="carrito_eliminar"),
    path("carrito/actualizar/<int:producto_id>/", views.carrito_actualizar, name="carrito_actualizar"),

    # checkout público
    path("checkout/", views.CheckoutPublicoView.as_view(), name="checkout_publico"),
]
