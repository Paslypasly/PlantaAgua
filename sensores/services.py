# sensores/services.py
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Sensor, LecturaSensor, Alerta, ReglaControl, Actuador

User = get_user_model()

# ==========================================================
# REGISTRO DE LECTURAS AUTOMÁTICAS (MQTT / REST)
# ==========================================================
def registrar_lectura(sensor_codigo: str, valor: float):
    """
    Registrar lectura de un sensor desde JSON MQTT o REST.
    Ignora sensores desactivados o inexistentes.
    """
    try:
        sensor = Sensor.objects.get(codigo=sensor_codigo)
    except Sensor.DoesNotExist:
        print(f"⚠️ Sensor {sensor_codigo} no existe en BD.")
        return None

    # Si el sensor está desactivado → no procesa nada
    if not sensor.activo:
        print(f"⛔ Sensor {sensor.codigo} está desactivado. Lectura ignorada.")
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

    sensor.save(update_fields=["estado"])
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
        elif regla.condicion == "MENOR" and valor < regla.umbral:
            _generar_alerta(sensor, regla.mensaje, "WARNING")
            regla.actuador.estado_on = False
            regla.actuador.save()
        elif regla.condicion == "IGUAL" and valor == regla.umbral:
            _generar_alerta(sensor, regla.mensaje, "INFO")
            regla.actuador.estado_on = False
            regla.actuador.save()


# ==========================================================
# FUNCIONES ADMINISTRATIVAS
# ==========================================================
def forzar_actuador(actuador_id: int, estado: bool, usuario: User):
    """Forzar encendido/apagado de actuadores (solo ADMIN)."""
    actuador = Actuador.objects.get(pk=actuador_id)
    actuador.estado_on = estado
    actuador.save(update_fields=["estado_on"])
    Alerta.objects.create(
        sensor=None,
        mensaje=f"{usuario.username} forzó {actuador.nombre} a {'ON' if estado else 'OFF'}",
        severidad="INFO",
    )
    return actuador


def activar_sensor(sensor_id: int, activo: bool, usuario: User):
    """Activa o desactiva un sensor desde el panel ADMIN."""
    sensor = Sensor.objects.get(pk=sensor_id)
    sensor.activo = activo
    sensor.save(update_fields=["activo"])
    Alerta.objects.create(
        sensor=sensor,
        mensaje=f"{usuario.username} {'activó' if activo else 'desactivó'} el sensor {sensor.codigo}",
        severidad="INFO",
    )
    return sensor


def actualizar_umbrales(sensor_id: int, rango_min: Decimal, rango_max: Decimal, usuario: User):
    """Actualiza umbrales críticos manualmente."""
    sensor = Sensor.objects.get(pk=sensor_id)
    sensor.rango_min = rango_min
    sensor.rango_max = rango_max
    sensor.save(update_fields=["rango_min", "rango_max"])
    Alerta.objects.create(
        sensor=sensor,
        mensaje=f"{usuario.username} ajustó umbrales ({rango_min} - {rango_max})",
        severidad="INFO",
    )
    return sensor
