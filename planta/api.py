from django.http import JsonResponse
from .models import Estanque

def estado_estanques_api(request):
    estanques = Estanque.objects.all()
    data = {
        "estanques": [
            {
                "id": e.id,
                "nombre": e.nombre,
                "volumen_actual_litros": float(e.volumen_actual_litros),
                "nivel_porcentaje": float(e.nivel_porcentaje),
                "estado": e.estado or "SIN ESTADO",
            }
            for e in estanques
        ]
    }
    return JsonResponse(data)
