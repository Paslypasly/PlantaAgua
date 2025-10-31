from decimal import Decimal, InvalidOperation
from django.db import transaction
from calidad.models import Medicion, Alarma, AlarmaLog, Lote

def _cmp(cond, valor: Decimal, umbral: Decimal) -> bool:
    if cond == ">":  return valor > umbral
    if cond == "<":  return valor < umbral
    if cond == ">=": return valor >= umbral
    if cond == "<=": return valor <= umbral
    if cond == "==": return valor == umbral
    if cond == "!=": return valor != umbral
    return False

@transaction.atomic
def registrar_medicion_y_evaluar(*, planta, sensor, valor, unidad, lote_codigo: str | None = None, ts=None):
    try:
        valor = Decimal(str(valor))
    except (InvalidOperation, TypeError):
        raise ValueError("Valor de medición inválido")
    lote = None
    if lote_codigo:
        try:
            lote = Lote.objects.select_for_update().get(planta=planta, codigo=lote_codigo)
        except Lote.DoesNotExist:
            lote = None
    med = Medicion.objects.create(
        planta=planta, sensor=sensor, lote=lote, valor=valor,
        unidad=unidad or sensor.unidad, timestamp=ts or None,
    )
    alarms = Alarma.objects.filter(planta=planta, activa=True)
    for al in alarms:
        regla_upper = (al.regla or "").upper()
        if sensor.tipo.upper() not in regla_upper and any(s in regla_upper for s in ("PH","TDS","UVI","ORP","NIVEL","CAUDAL","PRESION")):
            continue
        if _cmp(al.condicion, valor, al.umbral):
            AlarmaLog.objects.create(alarma=al, planta=planta, sensor=sensor, valor=valor, estado="abierta")
            if sensor.tipo in ("tds","uvi") and al.severidad in ("high",):
                if lote and lote.estado != "bloqueado":
                    lote.estado = "bloqueado"; lote.save(update_fields=["estado"])
                else:
                    abierto = Lote.objects.filter(planta=planta, estado="abierto").first()
                    if abierto: abierto.estado = "bloqueado"; abierto.save(update_fields=["estado"])
    return med
