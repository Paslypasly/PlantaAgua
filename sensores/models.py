# sensores/models.py
from django.db import models
from django.utils import timezone
from core.models import BaseModel


# ======================================================
#   TIPO DE SENSOR
# ======================================================
class TipoSensor(BaseModel):
    CODIGO_CHOICES = [
        ("NIVEL", "Sensor de nivel"),
        ("CONTADOR", "Sensor contador IR"),
        ("PH", "Sensor de pH"),
        ("OTRO", "Otro tipo de sensor"),
    ]

    codigo = models.CharField(max_length=20, choices=CODIGO_CHOICES, unique=True)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.get_codigo_display()}"


# ======================================================
#   SENSOR FÍSICO
# ======================================================
class Sensor(BaseModel):
    ESTADO_CHOICES = [
        ("OK", "OK"),
        ("FUERA_RANGO", "Fuera de rango"),
        ("SIN_DATOS", "Sin datos"),
    ]

    tipo = models.ForeignKey(TipoSensor, on_delete=models.PROTECT, related_name="sensores")
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
    codigo = models.CharField(max_length=50, unique=True)
    unidad = models.CharField(max_length=20)
    rango_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rango_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="SIN_DATOS")

    # Sensor de pH desactivado por defecto
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo

    def ultima_lectura(self):
        return self.lecturas.order_by("-fecha_hora").first()


# ======================================================
#   LECTURAS
# ======================================================
class LecturaSensor(BaseModel):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="lecturas"
    )
    fecha_hora = models.DateTimeField(default=timezone.now)
    valor = models.DecimalField(max_digits=12, decimal_places=3)
    calidad = models.CharField(max_length=20, blank=True)
    severidad = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ("-fecha_hora",)

    def __str__(self):
        return f"{self.sensor.codigo} = {self.valor} {self.sensor.unidad}"


# ======================================================
#   ACTUADOR (bomba, válvula, etc.)
# ======================================================
class Actuador(BaseModel):
    TIPO_CHOICES = [
        ("BOMBA", "Bomba de agua"),
        ("VALVULA", "Válvula"),
        ("RELE", "Relé"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    estado_on = models.BooleanField(default=False)  # ON/OFF lógico

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


# ======================================================
#   ALERTAS
# ======================================================
class Alerta(BaseModel):
    SEVERIDAD_CHOICES = [
        ("INFO", "Informativa"),
        ("WARNING", "Advertencia"),
        ("CRITICA", "Crítica"),
    ]

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="alertas"
    )
    mensaje = models.CharField(max_length=250)
    severidad = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES)
    atendida = models.BooleanField(default=False)

    def __str__(self):
        return f"Alerta {self.severidad} - {self.sensor.codigo}"


# ======================================================
#   REGLAS DE CONTROL
# ======================================================
class ReglaControl(BaseModel):
    CONDICION_CHOICES = [
        ("MAYOR", "Valor mayor a"),
        ("MENOR", "Valor menor a"),
        ("IGUAL", "Valor igual a"),
    ]

    nombre = models.CharField(max_length=100)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="reglas")
    condicion = models.CharField(max_length=20, choices=CONDICION_CHOICES)
    umbral = models.DecimalField(max_digits=10, decimal_places=2)
    actuador = models.ForeignKey(
        Actuador,
        on_delete=models.PROTECT,
        related_name="reglas"
    )
    mensaje = models.CharField(max_length=200, default="Condición de regla cumplida")

    def __str__(self):
        return f"{self.nombre} ({self.sensor.codigo})"
