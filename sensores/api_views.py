# sensores/api_views.py
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .services import registrar_lectura
from sensores.models import Sensor, ReglaControl, LecturaCrudaESP32
from .api_serializers import (
    SensorSerializer,
    ReglaControlSerializer,
    LecturaSensorSerializer,
    LecturaESP32Serializer,
)


# ============================================================
#   API REST EXISTENTE (lista / detalle sensores y reglas)
# ============================================================

class SensorListAPIView(generics.ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class ReglaControlListCreateAPIView(generics.ListCreateAPIView):
    queryset = ReglaControl.objects.all()
    serializer_class = ReglaControlSerializer


class RegistrarLecturaAPIView(APIView):
    """
    POST /api/iot/lecturas/
    (API antigua que ya usas, la dejamos por compatibilidad)
    """
    def post(self, request):
        serializer = LecturaSensorSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        sensor_codigo = data["sensor_codigo"]
        valor = data["valor"]

        lectura = registrar_lectura(sensor_codigo, valor)

        if lectura is None:
            return Response(
                {"error": "Sensor no encontrado o inactivo"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "mensaje": "Lectura registrada",
                "sensor": sensor_codigo,
                "valor": str(valor)
            },
            status=status.HTTP_201_CREATED
        )


# ============================================================
#   NUEVA API PARA ESP32 (prompt maestro)
# ============================================================

class RegistrarLecturaESP32APIView(APIView):
    """
    POST /api/sensores/lectura/
    JSON esperado (EXACTO):

    {
      "token": "TOKEN_SUPER_SECRETO",
      "sensor_id": "tanque_1",
      "nivel_cm": 118.55,
      "ir_estado": 0,
      "ph": null
    }
    """

    def post(self, request):
        serializer = LecturaESP32Serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # 1) Validar TOKEN
        token_recibido = data["token"]
        token_esperado = getattr(settings, "SENSORES_API_TOKEN", None)

        if not token_esperado or token_recibido != token_esperado:
            return Response(
                {"error": "Token inválido o no configurado"},
                status=status.HTTP_403_FORBIDDEN
            )

        sensor_id = data["sensor_id"]
        nivel_cm = data.get("nivel_cm")
        ir_estado = data.get("ir_estado")
        ph = data.get("ph")
        timestamp = data.get("timestamp") or timezone.now()

        # 2) Guardar lectura cruda para auditoría
        lectura_cruda = LecturaCrudaESP32.objects.create(
            sensor_id=sensor_id,
            nivel_cm=nivel_cm,
            ir_estado=ir_estado,
            ph=ph,
            timestamp=timestamp,
        )

        # 3) Mapear a tus sensores reales (Sensor + LecturaSensor)
        resultados = []

        # Convención: tanque_1_NIVEL, tanque_1_IR, tanque_1_PH
        if nivel_cm is not None:
            codigo_nivel = f"{sensor_id}_NIVEL"
            lectura_nivel = registrar_lectura(codigo_nivel, float(nivel_cm))
            resultados.append(
                {"sensor_codigo": codigo_nivel, "valor": str(nivel_cm),
                 "ok": lectura_nivel is not None}
            )

        if ir_estado is not None:
            codigo_ir = f"{sensor_id}_IR"
            lectura_ir = registrar_lectura(codigo_ir, float(ir_estado))
            resultados.append(
                {"sensor_codigo": codigo_ir, "valor": str(ir_estado),
                 "ok": lectura_ir is not None}
            )

        if ph is not None:
            codigo_ph = f"{sensor_id}_PH"
            lectura_ph = registrar_lectura(codigo_ph, float(ph))
            resultados.append(
                {"sensor_codigo": codigo_ph, "valor": str(ph),
                 "ok": lectura_ph is not None}
            )

        return Response(
            {
                "mensaje": "Lectura ESP32 procesada",
                "sensor_id": sensor_id,
                "timestamp": timestamp,
                "resultados": resultados,
            },
            status=status.HTTP_201_CREATED
        )


class SensoresDashboardAPIView(APIView):
    """
    GET /api/sensores/dashboard/
    Mini-dashboard JSON con resumen por sensor_id del ESP32.
    Sirve para pruebas rápidas y para tu informe.
    """

    def get(self, request):
        from django.db.models import Max, Avg, Count

        qs = LecturaCrudaESP32.objects.all()

        # Resumen por sensor_id
        resumen = (
            qs.values("sensor_id")
            .annotate(
                lecturas=Count("id"),
                ultima_medicion=Max("timestamp"),
                nivel_promedio=Avg("nivel_cm"),
            )
            .order_by("sensor_id")
        )

        return Response(
            {
                "total_lecturas": qs.count(),
                "sensores": list(resumen),
            },
            status=status.HTTP_200_OK
        )
