# sensores/models.py
from django.db import models
from core.models import BaseModel


class TipoSensor(BaseModel):
    CODIGO_CHOICES = [
        ("NIVEL", "Nivel"),
        ("CONTADOR", "Contador"),
        ("PH", "pH"),
        ("OTRO", "Otro"),
    ]

    codigo = models.CharField(
        max_length=20,
        choices=CODIGO_CHOICES,
        unique=True
    )
    descripcion = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.descripcion


class Sensor(BaseModel):
    tipo = models.ForeignKey(
        TipoSensor,
        on_delete=models.PROTECT,
        related_name="sensores"
    )
    estanque = models.ForeignKey(
        "planta.Estanque",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sensores"
    )
    ubicacion = models.ForeignKey(
        "inventario.Ubicacion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sensores"
    )
    codigo = models.CharField(
        max_length=50,
        unique=True,
        help_text="Identificador lógico del sensor (ej. NIVEL_CRUDO_01)."
    )
    unidad = models.CharField(max_length=20)
    rango_min = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    rango_max = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.codigo

    def ultima_lectura(self):
        return self.lecturas.order_by("-fecha_hora").first()


class LecturaSensor(BaseModel):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="lecturas"
    )
    fecha_hora = models.DateTimeField()
    valor = models.DecimalField(max_digits=12, decimal_places=3)
    calidad = models.CharField(max_length=20, blank=True)
    severidad = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ("-fecha_hora",)

    def __str__(self) -> str:
        return f"{self.sensor.codigo} = {self.valor} {self.sensor.unidad} @ {self.fecha_hora}"
