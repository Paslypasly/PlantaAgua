# planta/models.py
from django.db import models

try:
    from core.models import BaseModel
except Exception:
    BaseModel = models.Model


class Estanque(BaseModel):
    TIPO_CHOICES = (
        ("CRUDO", "Agua cruda"),
        ("PURIFICADA", "Agua purificada"),
    )

    nombre = models.CharField(max_length=120, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="CRUDO")
    capacidad_litros = models.FloatField(default=1.0)

    nivel_agua = models.FloatField(default=0.0)
    estado = models.CharField(max_length=30, blank=True, default="OK")

    ph_actual = models.FloatField(null=True, blank=True)
    ph_raw = models.IntegerField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def volumen_actual_litros(self):
        return float(self.nivel_agua or 0)

    @property
    def nivel_porcentaje(self):
        cap = float(self.capacidad_litros or 0)
        if cap <= 0:
            return 0
        return round((float(self.nivel_agua or 0) / cap) * 100, 2)

    def __str__(self):
        return self.nombre


class EventoPlanta(BaseModel):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class InventarioBidones(BaseModel):
    class Modo(models.TextChoices):
        NONE = "NONE", "Sin acción"
        IN = "IN", "Ingreso (+)"
        OUT = "OUT", "Salida (-)"

    class Tipo(models.TextChoices):
        L10 = "L10", "Bidón 10L"
        L20 = "L20", "Bidón 20L"

    stock_10 = models.IntegerField(default=0)
    stock_20 = models.IntegerField(default=0)

    modo_pendiente = models.CharField(max_length=10, choices=Modo.choices, default=Modo.NONE)
    tipo_pendiente = models.CharField(max_length=10, choices=Tipo.choices, default=Tipo.L10)

    ultimo_contador_esp = models.IntegerField(default=0)
    ultima_accion = models.CharField(max_length=255, blank=True, default="")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventario(10={self.stock_10},20={self.stock_20},modo={self.modo_pendiente},tipo={self.tipo_pendiente},esp={self.ultimo_contador_esp})"
