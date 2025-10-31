from django.urls import path
from . import web_views

urlpatterns = [
    path('pedidos/', web_views.pedidos_list, name='web_pedidos_list'),
    path('pedidos/nuevo/', web_views.pedido_new, name='web_pedido_new'),
    path('pedidos/<int:pk>/', web_views.pedido_detail, name='web_pedido_detail'),
    path('clientes/', web_views.clientes_list, name='web_clientes_list'),
    path('clientes/nuevo/', web_views.cliente_new, name='web_cliente_new'),
]
