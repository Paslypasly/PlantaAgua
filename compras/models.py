# compras/models.py
from django.db import models
from core.models import BaseModel


class OrdenCompra(BaseModel):
    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("RECEPCIONADA", "Recepcionada"),
        ("CANCELADA", "Cancelada"),
    ]

    numero = models.CharField(max_length=20, unique=True)
    proveedor = models.ForeignKey(
        "proveedores.Proveedor",
        on_delete=models.PROTECT,
        related_name="ordenes_compra"
    )
    fecha = models.DateField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="PENDIENTE"
    )
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"OC {self.numero}"

    def calcular_total(self):
        total = sum(det.subtotal for det in self.detalles.all())
        self.total = total
        return total


class DetalleOrdenCompra(BaseModel):
    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    insumo = models.ForeignKey(
        "inventario.Insumo",
        on_delete=models.PROTECT
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.costo_unitario

    def __str__(self) -> str:
        return f"{self.cantidad} x {self.insumo} (OC {self.orden_compra.numero})"
