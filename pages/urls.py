# pages/urls.py
from django.urls import path
from .views import HomeView, AcercaView, AyudaView, ContactoView, SoporteView

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("acerca/", AcercaView.as_view(), name="acerca"),
    path("ayuda/", AyudaView.as_view(), name="ayuda"),
    path("contacto/", ContactoView.as_view(), name="contacto"),
    path("soporte/", SoporteView.as_view(), name="soporte"),
]
