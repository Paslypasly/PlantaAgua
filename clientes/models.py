# clientes/models.py
from django.db import models
from django.db.models import Q
from core.models import BaseModel, EntidadConRut


class SectorEntrega(BaseModel):
    nombre = models.CharField(max_length=50)
    recargo_delivery = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.nombre


class Cliente(EntidadConRut):
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    sector_entrega = models.ForeignKey(
        SectorEntrega,
        on_delete=models.PROTECT,
        related_name="clientes"
    )

    def __str__(self):
        return f"{self.nombre} ({self.rut_completo})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["rut", "dv"],
                name="uq_rut_dv_cliente",
                condition=Q(rut__isnull=False),
            )
        ]
