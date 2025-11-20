# sensores/services.py
from decimal import Decimal
from django.utils import timezone
from .models import Sensor, LecturaSensor, Alerta, ReglaControl


def registrar_lectura(sensor_codigo: str, valor: float):
    """
    Registrar lectura de un sensor desde JSON MQTT o REST.
    Genera alertas automáticas si corresponde.
    Evalúa reglas de control.
    """
    try:
        sensor = Sensor.objects.get(codigo=sensor_codigo, activo=True)
    except Sensor.DoesNotExist:
        return None

    lectura = LecturaSensor.objects.create(
        sensor=sensor,
        valor=Decimal(valor),
        fecha_hora=timezone.now()
    )

    # Evaluar estado del sensor
    if sensor.rango_min is not None and valor < sensor.rango_min:
        sensor.estado = "FUERA_RANGO"
        _generar_alerta(sensor, f"Valor bajo: {valor}", "WARNING")
    elif sensor.rango_max is not None and valor > sensor.rango_max:
        sensor.estado = "FUERA_RANGO"
        _generar_alerta(sensor, f"Valor alto: {valor}", "CRITICA")
    else:
        sensor.estado = "OK"

    sensor.save()
    evaluar_reglas(sensor, valor)

    return lectura


def _generar_alerta(sensor, mensaje, severidad):
    return Alerta.objects.create(
        sensor=sensor,
        mensaje=mensaje,
        severidad=severidad
    )


def evaluar_reglas(sensor, valor):
    reglas = sensor.reglas.all()

    for regla in reglas:
        if regla.condicion == "MAYOR" and valor > regla.umbral:
            _generar_alerta(sensor, regla.mensaje, "CRITICA")
            regla.actuador.estado_on = True
            regla.actuador.save()

        if regla.condicion == "MENOR" and valor < regla.umbral:
            _generar_alerta(sensor, regla.mensaje, "WARNING")
            regla.actuador.estado_on = False
            regla.actuador.save()

        if regla.condicion == "IGUAL" and valor == regla.umbral:
            _generar_alerta(sensor, regla.mensaje, "INFO")
            regla.actuador.estado_on = False
            regla.actuador.save()
