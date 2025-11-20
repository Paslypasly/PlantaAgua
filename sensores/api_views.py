# sensores/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .services import registrar_lectura
from sensores.models import Sensor, ReglaControl
from .api_serializers import SensorSerializer, ReglaControlSerializer, LecturaSensorSerializer


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
    Recibe JSON desde ESP32 o Postman.
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
