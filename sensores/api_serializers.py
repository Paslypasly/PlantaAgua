# sensores/api_serializers.py
from rest_framework import serializers

from sensores.models import Sensor, ReglaControl, LecturaCrudaESP32


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"


class ReglaControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReglaControl
        fields = "__all__"


class LecturaSensorSerializer(serializers.Serializer):
    # Serializer antiguo (por si ya lo usas)
    sensor_codigo = serializers.CharField()
    valor = serializers.DecimalField(max_digits=12, decimal_places=3)
    unidad = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=False)


class LecturaESP32Serializer(serializers.Serializer):
    """
    Serializer alineado EXACTAMENTE al JSON del prompt maestro.
    Este es el que va a usar el ESP32.
    """
    token = serializers.CharField()
    sensor_id = serializers.CharField()
    nivel_cm = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    ir_estado = serializers.IntegerField(required=False, allow_null=True)
    ph = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)
    timestamp = serializers.DateTimeField(required=False, allow_null=True)
