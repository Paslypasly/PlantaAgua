# ventas/models.py
from django.db import models
from core.models import BaseModel


class Pedido(BaseModel):
    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("EN_RUTA", "En ruta"),
        ("ENTREGADO", "Entregado"),
        ("CANCELADO", "Cancelado"),
    ]

    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="pedidos"
    )
    sector_entrega = models.ForeignKey(
        "clientes.SectorEntrega",
        on_delete=models.PROTECT,
        related_name="pedidos"
    )
    fecha = models.DateField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="PENDIENTE"
    )
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"Pedido {self.numero}"

    def calcular_total(self) -> float:
        total = sum(det.subtotal for det in self.detalles.all())
        self.total = total
        return total


class DetallePedido(BaseModel):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self) -> float:
        return self.cantidad * self.precio_unitario

    def __str__(self) -> str:
        return f"{self.cantidad} x {self.producto} (Pedido {self.pedido.numero})"
