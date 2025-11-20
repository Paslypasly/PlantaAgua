from django.urls import path
from .views import ClienteListView, ClienteCreateView

urlpatterns = [
    path("", ClienteListView.as_view(), name="clientes_lista"),
    path("nuevo/", ClienteCreateView.as_view(), name="cliente_nuevo"),
]
