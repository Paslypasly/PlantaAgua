from django.contrib import admin
from .models import Estanque

@admin.register(Estanque)
class EstanqueAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "capacidad_litros")
