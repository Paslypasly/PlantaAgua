from django.urls import path
from .views import NotificacionListView, NotificacionMarcarLeidasView

app_name = "notificaciones"

urlpatterns = [
    path("", NotificacionListView.as_view(), name="lista"),
    path("marcar-leidas/", NotificacionMarcarLeidasView.as_view(), name="marcar_leidas"),
]
