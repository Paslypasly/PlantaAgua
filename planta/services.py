# planta/services.py
from django.utils import timezone
from planta.models import Estanque
from sensores.models import Sensor, Alerta, LecturaSensor


def obtener_resumen_planta():
    """
    Retorna datos agregados para el dashboard:
    - estanques
    - total sensores
    - lecturas de hoy
    - alertas activas
    """
    hoy = timezone.now().date()

    estanques = Estanque.objects.all()
    total_sensores = Sensor.objects.count()
    lecturas_hoy = LecturaSensor.objects.filter(fecha_hora__date=hoy).count()
    alertas_activas = Alerta.objects.filter(atendida=False).order_by("-created_at")[:10]

    return {
        "estanques": estanques,
        "total_sensores": total_sensores,
        "lecturas_hoy": lecturas_hoy,
        "alertas_activas": alertas_activas,
    }
