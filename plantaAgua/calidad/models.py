from django.conf import settings
from django.db import models
from django.utils import timezone


LOTE_ESTADOS = (
    ("abierto", "Abierto"),
    ("cerrado", "Cerrado"),
    ("bloqueado", "Bloqueado"),  # por fuera de rango
)

AL_SEVERIDAD = (
    ("info", "Info"),
    ("warn", "Advertencia"),
    ("high", "Alta"),
)

AL_ESTADO = (
    ("abierta", "Abierta"),
    ("reconocida", "Reconocida"),
    ("cerrada", "Cerrada"),
)


class Lote(models.Model):
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.PROTECT)
    codigo = models.CharField(max_length=40, unique=True)      # ej "L-2025-10-30-001"
    fecha = models.DateTimeField(default=timezone.now)
    estacion = models.ForeignKey("iot.EstacionLlenado", on_delete=models.PROTECT)
    operador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    volumen_real_l = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    tds = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    uvi = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    orp = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    estado = models.CharField(max_length=12, choices=LOTE_ESTADOS, default="abierto")

    class Meta:
        indexes = [
            models.Index(fields=["planta", "fecha"]),
            models.Index(fields=["estado"]),
        ]

    def __str__(self):
        return f"Lote {self.codigo} ({self.planta.codigo})"


class Medicion(models.Model):
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.PROTECT)
    sensor = models.ForeignKey("iot.Sensor", on_delete=models.PROTECT)
    lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=14, decimal_places=5)
    unidad = models.CharField(max_length=15)
    timestamp = models.DateTimeField(default=timezone.now)
    calidad_ok = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["planta", "timestamp"]),
            models.Index(fields=["sensor", "timestamp"]),
        ]

    def save(self, *args, **kwargs):
        # Auto-evaluación calidad_ok según rango del sensor si existe
        try:
            if self.sensor.rango_min is not None and self.sensor.rango_max is not None:
                self.calidad_ok = (self.sensor.rango_min <= self.valor <= self.sensor.rango_max)
        except Exception:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sensor.tipo.upper()}={self.valor} {self.unidad} @ {self.timestamp:%Y-%m-%d %H:%M}"


class Alarma(models.Model):
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.PROTECT)
    regla = models.CharField(max_length=100)                   # ej: "TDS>100", "UVI<0.4"
    condicion = models.CharField(max_length=20)                # ">", "<", ">=", "<=", "!="
    umbral = models.DecimalField(max_digits=14, decimal_places=5)
    severidad = models.CharField(max_length=10, choices=AL_SEVERIDAD, default="warn")
    activa = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["planta", "activa"]),
            models.Index(fields=["severidad"]),
        ]

    def __str__(self):
        return f"[{self.severidad.upper()}] {self.regla}"


class AlarmaLog(models.Model):
    alarma = models.ForeignKey(Alarma, on_delete=models.CASCADE)
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.PROTECT)
    sensor = models.ForeignKey("iot.Sensor", on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=14, decimal_places=5, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=15, choices=AL_ESTADO, default="abierta")

    class Meta:
        indexes = [
            models.Index(fields=["planta", "timestamp"]),
            models.Index(fields=["estado"]),
        ]

    def __str__(self):
        return f"{self.alarma} @ {self.timestamp:%Y-%m-%d %H:%M}"


class ChecklistPH(models.Model):
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.PROTECT)
    fecha = models.DateField(default=timezone.now)
    valor_ph = models.DecimalField(max_digits=6, decimal_places=3)
    evidencia_url = models.TextField(blank=True)               # URL de imagen/archivo en storage
    firmado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        unique_together = [("planta", "fecha")]
        indexes = [
            models.Index(fields=["planta", "fecha"]),
        ]

    def __str__(self):
        return f"Checklist pH {self.fecha} @ {self.planta.codigo}"
