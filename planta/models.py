# planta/models.py
from django.db import models
from core.models import BaseModel


class Estanque(BaseModel):
    TIPO_CHOICES = [
        ("CRUDO", "Agua cruda"),
        ("PURIFICADA", "Agua purificada"),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidad_litros = models.PositiveIntegerField()
    nivel_agua = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Nivel actual de agua en litros (aprox.)."
    )
    ubicacion = models.ForeignKey(
        "inventario.Ubicacion",
        on_delete=models.PROTECT,
        related_name="estanques",
        null=True,
        blank=True,
    )
    estado = models.CharField(max_length=50, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.nombre

    @property
    def porcentaje_ocupacion(self) -> float:
        if self.capacidad_litros == 0:
            return 0
        return float(self.nivel_agua) / float(self.capacidad_litros) * 100


class Bomba(BaseModel):
    nombre = models.CharField(max_length=100)
    estanque_origen = models.ForeignKey(
        Estanque,
        on_delete=models.PROTECT,
        related_name="bombas_origen"
    )
    estanque_destino = models.ForeignKey(
        Estanque,
        on_delete=models.PROTECT,
        related_name="bombas_destino"
    )
    modo_automatico = models.BooleanField(default=True)
    estado_on = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nombre

    @property
    def estado_operativo(self) -> str:
        return "ON" if self.estado_on else "OFF"


class ConfiguracionPlanta(BaseModel):
    estanque = models.ForeignKey(
        Estanque,
        on_delete=models.CASCADE,
        related_name="configuraciones"
    )
    nivel_min_operacion = models.DecimalField(max_digits=10, decimal_places=2)
    nivel_max_operacion = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Config {self.estanque.nombre}"
