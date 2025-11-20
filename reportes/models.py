# reportes/models.py
from django.db import models
from django.conf import settings
from core.models import BaseModel


class ReporteGenerado(BaseModel):
    TIPO_CHOICES = [
        ("PRODUCCION", "Reporte de producción"),
        ("VENTAS", "Reporte de ventas"),
        ("INVENTARIO", "Reporte de inventario"),
        ("ALERTAS", "Reporte de alertas"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    generado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reportes_generados"
    )
    parametros = models.JSONField(
        null=True,
        blank=True,
        help_text="Filtros usados al generar el reporte (fechas, cliente, etc.)."
    )

    def __str__(self) -> str:
        return f"{self.get_tipo_display()} #{self.id}"
