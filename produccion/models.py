from django.db import models
from core.models import BaseModel

class LoteProduccion(BaseModel):
    fecha = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    estanque = models.ForeignKey(
        "planta.Estanque",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    litros = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("PENDIENTE", "Pendiente"),
            ("EN_PROCESO", "En proceso"),
            ("FINALIZADO", "Finalizado"),
        ],
        default="PENDIENTE"
    )
    observaciones = models.TextField(blank=True)


    def __str__(self):
        return f"Lote {self.id} - {self.fecha}"

    # 👇 Inserta este bloque justo aquí
    @property
    def litros_producidos(self):
        """
        Alias para compatibilidad con plantillas antiguas.
        Devuelve el mismo valor que 'litros'.
        """
        return self.litros

