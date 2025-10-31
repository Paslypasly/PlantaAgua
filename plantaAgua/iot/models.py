from django.db import models

SENSOR_TIPOS = (
    ("ph", "pH"),
    ("tds", "TDS"),
    ("uvi", "UV Intensity"),
    ("orp", "ORP"),
    ("nivel", "Nivel"),
    ("caudal", "Caudal"),
    ("presion", "Presión"),
)

SEPARADORES = 120  # ancho sugerido para __str__ si lo usas en admin


class Equipo(models.Model):
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)                     # ej: "Bomba", "Filtro", "UV", "Ozono"
    modelo = models.CharField(max_length=50, blank=True)
    serie = models.CharField(max_length=50, blank=True)
    ubicacion = models.CharField(max_length=120, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["planta", "tipo"]),
        ]

    def __str__(self):
        return f"{self.tipo} ({self.modelo}) @ {self.planta.codigo}"


class Sensor(models.Model):
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=30, choices=SENSOR_TIPOS)
    unidad = models.CharField(max_length=15)                   # ej: "pH", "ppm", "mV", "mW/cm2"
    topico_mqtt = models.CharField(max_length=160, unique=True)
    rango_min = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    rango_max = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    calibracion = models.JSONField(default=dict, blank=True)   # {offset: x, slope: y, puntos: [...]}
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = [("planta", "tipo", "topico_mqtt")]
        indexes = [
            models.Index(fields=["planta", "tipo"]),
            models.Index(fields=["activo"]),
        ]

    def __str__(self):
        return f"{self.tipo.upper()} [{self.topico_mqtt}]"


class EstacionLlenado(models.Model):
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    caudal_nominal_lpm = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    class Meta:
        unique_together = [("planta", "nombre")]
        indexes = [
            models.Index(fields=["planta"]),
        ]

    def __str__(self):
        return f"{self.nombre} @ {self.planta.codigo}"
