from django.urls import path
from . import api_views

urlpatterns = [
    path("pedidos/<int:pedido_id>/estado", api_views.actualizar_estado, name="api_pedido_estado"),
    path("pedidos/<int:pedido_id>/tracking", api_views.ver_tracking, name="api_pedido_tracking"),
]
