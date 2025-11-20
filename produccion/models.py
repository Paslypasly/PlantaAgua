# produccion/models.py
from django.db import models
from core.models import BaseModel


class LoteProduccion(BaseModel):
    codigo = models.CharField(max_length=30, unique=True)
    estanque_origen = models.ForeignKey(
        "planta.Estanque",
        on_delete=models.PROTECT,
        related_name="lotes_origen"
    )
    volumen_litros = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    observaciones = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.codigo
