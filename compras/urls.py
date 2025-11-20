# compras/urls.py
from django.urls import path
from .views import OrdenCompraListView, OrdenCompraCreateView

urlpatterns = [
    path("ordenes/", OrdenCompraListView.as_view(), name="compras_ordenes"),
    path("ordenes/nueva/", OrdenCompraCreateView.as_view(), name="compras_orden_nueva"),
]
