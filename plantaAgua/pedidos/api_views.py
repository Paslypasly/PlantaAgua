import json
from decimal import Decimal
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Pedido, PedidoTracking, ESTADOS_PEDIDO
from .utils import require_api_key

ESTADOS_VALIDOS = {c for c, _ in ESTADOS_PEDIDO}  # {"RECIBIDO","PREPARACION","EN_RUTA","ENTREGADO","FALLIDO"}

def _get_pedido_or_404(pedido_id: int) -> Pedido:
    try:
        return Pedido.objects.get(pk=pedido_id)
    except Pedido.DoesNotExist:
        raise Http404("Pedido no encontrado")

@csrf_exempt
@require_api_key
def actualizar_estado(request, pedido_id: int):
    """
    POST /api/pedidos/<id>/estado
    Body JSON: {"estado":"EN_RUTA","nota":"saliendo","lat":-20.123456,"lon":-70.234567}
    Header: X-API-KEY: <settings.API_MOBILE_KEY>
    """
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "method_not_allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    estado = (data.get("estado") or "").upper()
    if estado not in ESTADOS_VALIDOS:
        return JsonResponse({"ok": False, "error": "estado_invalido"}, status=400)

    ped = _get_pedido_or_404(pedido_id)

    # Actualiza estado si cambió
    if ped.estado != estado:
        ped.estado = estado
        ped.save(update_fields=["estado", "actualizado"])

    # Crear tracking
    nota = data.get("nota") or ""
    lat = data.get("lat")
    lon = data.get("lon")
    try:
        lat = Decimal(str(lat)) if lat is not None else None
        lon = Decimal(str(lon)) if lon is not None else None
    except Exception:
        return JsonResponse({"ok": False, "error": "lat_lon_invalidos"}, status=400)

    tr = PedidoTracking.objects.create(
        pedido=ped, estado=estado, timestamp=timezone.now(),
        nota=nota, lat=lat, lon=lon
    )

    return JsonResponse({
        "ok": True,
        "pedido": ped.pk,
        "estado": ped.estado,
        "tracking_id": tr.pk,
        "timestamp": tr.timestamp.isoformat(),
    })

@require_api_key
def ver_tracking(request, pedido_id: int):
    """
    GET /api/pedidos/<id>/tracking
    Header: X-API-KEY: <settings.API_MOBILE_KEY>
    """
    if request.method != "GET":
        return JsonResponse({"ok": False, "error": "method_not_allowed"}, status=405)

    ped = _get_pedido_or_404(pedido_id)
    eventos = ped.tracking.order_by("timestamp").values(
        "estado", "timestamp", "nota", "lat", "lon"
    )
    return JsonResponse({
        "ok": True,
        "pedido": ped.pk,
        "cliente": str(ped.cliente),
        "estado_actual": ped.estado,
        "historial": [
            {
                "estado": e["estado"],
                "timestamp": e["timestamp"].isoformat(),
                "nota": e["nota"],
                "lat": float(e["lat"]) if e["lat"] is not None else None,
                "lon": float(e["lon"]) if e["lon"] is not None else None,
            } for e in eventos
        ]
    })
