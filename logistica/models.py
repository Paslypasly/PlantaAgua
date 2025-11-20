# logistica/models.py
from django.db import models
from core.models import BaseModel
from django.conf import settings


class Vehiculo(BaseModel):
    patente = models.CharField(max_length=10, unique=True)
    marca_modelo = models.CharField(max_length=100)
    capacidad_carga_kg = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.patente} - {self.marca_modelo}"


class RutaEntrega(BaseModel):
    ESTADO_CHOICES = [
        ("ASIGNADA", "Asignada"),
        ("CARGADA", "Cargada"),
        ("EN_CAMINO", "En camino"),
        ("ENTREGADA", "Entregada"),
    ]

    fecha = models.DateField()
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        related_name="rutas"
    )
    # El modelo Usuario se definirá en app 'cuentas' en FASE 2.
    conductor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="rutas_conducidas"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="ASIGNADA"
    )

    def __str__(self) -> str:
        return f"Ruta {self.id} - {self.fecha} - {self.vehiculo.patente}"


class RutaPedido(BaseModel):
    ruta = models.ForeignKey(
        RutaEntrega,
        on_delete=models.CASCADE,
        related_name="ruta_pedidos"
    )
    pedido = models.ForeignKey(
        "ventas.Pedido",
        on_delete=models.PROTECT,
        related_name="rutas"
    )
    fecha_hora_estado = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("ruta", "pedido")

    def __str__(self) -> str:
        return f"Ruta {self.ruta_id} - Pedido {self.pedido_id}"
