# pages/urls.py
from django.urls import path
from .views import HomeView, AcercaView, SoporteView, ContactoView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("acerca/", AcercaView.as_view(), name="acerca"),
    path("soporte/", SoporteView.as_view(), name="soporte"),
    path("contacto/", ContactoView.as_view(), name="contacto"),
]
