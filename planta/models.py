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
    estado = models.CharField(
        max_length=50,
        blank=True,
        help_text="Estado operativo del estanque (OK, ALERTA, MANTENCION, etc.)."
    )
    observaciones = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.nombre

    @property
    def porcentaje_ocupacion(self) -> float:
        """
        Porcentaje de ocupación del estanque (0–100).
        """
        if self.capacidad_litros == 0:
            return 0
        return float(self.nivel_agua) / float(self.capacidad_litros) * 100

    # === ALIAS para que calcen con los templates ===

    @property
    def volumen_actual_litros(self) -> float:
        """
        Alias de nivel_agua para que los templates puedan usar
        'volumen_actual_litros' sin romper nada.
        """
        return float(self.nivel_agua or 0)

    @property
    def nivel_porcentaje(self) -> float:
        """
        Alias de porcentaje_ocupacion, usado en barras de progreso.
        """
        return self.porcentaje_ocupacion


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
        """
        Devuelve 'ON' o 'OFF' según el estado de la bomba.
        """
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


class EventoPlanta(BaseModel):
    """
    Eventos relevantes en la planta:
    - Paros / arranques
    - Mantenciones
    - Alertas manuales o automáticas
    """
    class Severidad(models.TextChoices):
        BAJA = "BAJA", "Baja"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"

    class TipoEvento(models.TextChoices):
        PARO = "PARO", "Paro"
        ARRANQUE = "ARRANQUE", "Arranque"
        MANTENCION = "MANTENCION", "Mantención"
        ALERTA = "ALERTA", "Alerta"
        OTRO = "OTRO", "Otro"

    fecha_hora = models.DateTimeField()
    tipo = models.CharField(max_length=50, choices=TipoEvento.choices)
    descripcion = models.TextField()
    estanque = models.ForeignKey(
        Estanque,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos"
    )
    severidad = models.CharField(
        max_length=10,
        choices=Severidad.choices,
        default=Severidad.BAJA,
    )

    def __str__(self) -> str:
        return f"{self.get_tipo_display()} · {self.fecha_hora:%d-%m-%Y %H:%M}"
