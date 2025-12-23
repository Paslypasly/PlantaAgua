# planta/views.py
import json
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from sensores.models import Sensor
from core.mixins import RolRequiredMixin
from .models import Estanque, InventarioBidones
from produccion.models import LoteProduccion



from sensores.models import Sensor

from sensores.models import Sensor

from django.utils import timezone
from django.views.generic import TemplateView
from core.mixins import RolRequiredMixin
from .models import Estanque, InventarioBidones
from sensores.models import Sensor


class EstadoEstanquesView(RolRequiredMixin, TemplateView):
    """
    Vista principal de monitoreo en planta.
    Muestra nivel, pH e inventario.
    Solo usa sensores activos vinculados a cada estanque.
    """
    template_name = "planta/estado_estanques.html"
    rol_requerido = None  # visible a cualquier usuario autenticado

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        estanques = Estanque.objects.all().order_by("nombre")

        for e in estanques:
            # Inicializamos estado por defecto
            e.sensor_nivel_activo = True
            e.sensor_ph_activo = True

            # Sensor de nivel asociado al estanque actual
            sensor_nivel = Sensor.objects.filter(
                tipo__codigo="NIVEL", estanque=e
            ).first()

            if sensor_nivel:
                if not sensor_nivel.activo:
                    e.sensor_nivel_activo = False
                    e.nivel_agua = None
                    e.nivel_porcentaje = 0
                    e.estado = "Sensor nivel desactivado"
            else:
                # Si no existe sensor nivel asociado
                e.sensor_nivel_activo = False

            # Sensor de pH asociado al estanque actual
            sensor_ph = Sensor.objects.filter(
                tipo__codigo="PH", estanque=e
            ).first()

            if sensor_ph:
                if not sensor_ph.activo:
                    e.sensor_ph_activo = False
                    e.ph_actual = None
                    e.estado = "Sensor pH desactivado"
            else:
                e.sensor_ph_activo = False

        # Inventario IR (no depende de sensores nivel/pH)
        inventario = InventarioBidones.objects.order_by("-updated_at").first()

        ctx.update({
            "hoy": timezone.localdate(),
            "estanques": estanques,
            "inventario": inventario,
        })
        return ctx







class ControlPlantaView(RolRequiredMixin, TemplateView):
    template_name = "planta/control_planta.html"
    rol_requerido = "OPERARIO"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["estanques"] = Estanque.objects.all().order_by("nombre")
        ctx["ultimos_lotes"] = LoteProduccion.objects.all().order_by("-fecha_creacion")[:5]
        return ctx


from django.http import JsonResponse
from django.utils.timezone import localtime
from sensores.models import Sensor
from .models import Estanque, InventarioBidones


def estado_estanques_api(request):
    """
    API: Devuelve el estado actual de los estanques e inventario IR.
    - Ignora sensores desactivados.
    - Sin cacheo (siempre valores actuales).
    """
    data = {"estanques": [], "inventario": None}

    estanques = Estanque.objects.all().order_by("nombre")

    for e in estanques:
        est_data = {
            "id": e.id,
            "nombre": e.nombre,
            "tipo": e.get_tipo_display(),
            "estado": e.estado,
            "capacidad_litros": float(e.capacidad_litros or 0),
            "volumen_actual_litros": float(e.volumen_actual_litros or 0),
            "nivel_porcentaje": float(e.nivel_porcentaje or 0),
            "ph": None,
            "ph_raw": None,
        }

        # Sensor de nivel asociado al estanque
        s_nivel = Sensor.objects.filter(tipo__codigo="NIVEL", estanque=e).first()
        if s_nivel:
            if not s_nivel.activo:
                est_data["estado"] = "Sensor nivel desactivado"
                est_data["nivel_porcentaje"] = 0
            else:
                # el valor viene desde modelo Estanque, actualizado por loop ESP32
                est_data["nivel_porcentaje"] = float(e.nivel_porcentaje or 0)

        # Sensor de pH asociado al estanque
        s_ph = Sensor.objects.filter(tipo__codigo="PH", estanque=e).first()
        if s_ph:
            if not s_ph.activo:
                est_data["estado"] = "Sensor pH desactivado"
            else:
                est_data["ph"] = float(e.ph_actual or 0)
                est_data["ph_raw"] = float(getattr(e, "ph_raw", 0))

        data["estanques"].append(est_data)

    # Inventario IR
    inv = InventarioBidones.objects.order_by("-updated_at").first()
    if inv:
        data["inventario"] = {
            "stock_10": inv.stock_10,
            "stock_20": inv.stock_20,
            "modo_pendiente": inv.modo_pendiente,
            "tipo_pendiente": inv.tipo_pendiente,
            "ultimo_contador_esp": inv.ultimo_contador_esp,
            "ultima_accion": inv.ultima_accion,
            "updated_at": localtime(inv.updated_at).strftime("%H:%M:%S"),
        }

    return JsonResponse(data)



@csrf_exempt
@require_POST
def inventario_set_selection_api(request):
    """
    body: {"mode":"IN|OUT|NONE", "type":"L10|L20"}
    """
    inv, _ = InventarioBidones.objects.get_or_create(id=1)

    try:
        payload = json.loads(request.body.decode("utf-8"))
        mode = (payload.get("mode") or inv.modo_pendiente or "NONE").upper()
        typ = (payload.get("type") or inv.tipo_pendiente or "L10").upper()
    except Exception:
        return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)

    if mode not in ("IN", "OUT", "NONE"):
        return JsonResponse({"ok": False, "error": "mode inválido"}, status=400)

    if typ not in ("L10", "L20"):
        return JsonResponse({"ok": False, "error": "type inválido"}, status=400)

    inv.modo_pendiente = mode
    inv.tipo_pendiente = typ
    inv.ultima_accion = f"Selección: {mode}/{typ}"
    inv.save(update_fields=["modo_pendiente", "tipo_pendiente", "ultima_accion", "updated_at"])

    return JsonResponse({"ok": True, "mode": inv.modo_pendiente, "type": inv.tipo_pendiente})
