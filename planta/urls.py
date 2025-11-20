# planta/urls.py
from django.urls import path
from .views import DashboardPlantaView

urlpatterns = [
    path("dashboard/", DashboardPlantaView.as_view(), name="dashboard_planta"),
]
