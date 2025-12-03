from django.urls import path
from .views import HomeView, AyudaView, ContactoView, AcercaView, SoporteView

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("ayuda/", AyudaView.as_view(), name="ayuda"),
    path("contacto/", ContactoView.as_view(), name="contacto"),
    path("acerca/", AcercaView.as_view(), name="acerca"),
    path("soporte/", SoporteView.as_view(), name="soporte"),
]
