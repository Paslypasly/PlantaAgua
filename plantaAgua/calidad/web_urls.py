from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.calidad_dashboard, name='web_calidad_dashboard'),
]
