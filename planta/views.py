# planta/views.py
import json
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from core.mixins import RolRequiredMixin
from .models import Estanque, InventarioBidones
from produccion.models import LoteProduccion


class EstadoEstanquesView(RolRequiredMixin, TemplateView):
    template_name = "planta/estado_estanques.html"
    rol_requerido = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        estanques = Estanque.objects.all().order_by("nombre")
        total_capacidad = sum(e.capacidad_litros for e in estanques)
        total_actual = sum(float(e.nivel_agua or 0) for e in estanques)

        inv, _ = InventarioBidones.objects.get_or_create(id=1)

        ctx["estanques"] = estanques
        ctx["total_capacidad"] = total_capacidad
        ctx["total_actual"] = total_actual
        ctx["porcentaje_global"] = (total_actual / total_capacidad * 100) if total_capacidad else 0
        ctx["inventario"] = inv
        return ctx


class ControlPlantaView(RolRequiredMixin, TemplateView):
    template_name = "planta/control_planta.html"
    rol_requerido = "OPERARIO"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["estanques"] = Estanque.objects.all().order_by("nombre")
        ctx["ultimos_lotes"] = LoteProduccion.objects.all().order_by("-fecha_creacion")[:5]
        return ctx


def estado_estanques_api(request):
    qs = Estanque.objects.all().order_by("nombre")
    inv, _ = InventarioBidones.objects.get_or_create(id=1)

    data = []
    for e in qs:
        data.append({
            "id": e.id,
            "nombre": e.nombre,
            "tipo": e.tipo,
            "capacidad_litros": e.capacidad_litros,
            "volumen_actual_litros": float(e.nivel_agua or 0),
            "nivel_porcentaje": float(e.nivel_porcentaje or 0),
            "estado": e.estado or "",
            "ph": float(e.ph_actual) if e.ph_actual is not None else None,
            "ph_raw": int(e.ph_raw) if e.ph_raw is not None else None,
        })

    return JsonResponse({
        "estanques": data,
        "inventario": {
            "stock_10": inv.stock_10,
            "stock_20": inv.stock_20,
            "modo_pendiente": inv.modo_pendiente,
            "tipo_pendiente": inv.tipo_pendiente,
            "ultimo_contador_esp": inv.ultimo_contador_esp,
            "ultima_accion": inv.ultima_accion,
        }
    })


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
