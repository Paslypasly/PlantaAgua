# sensores/api_serializers.py
from rest_framework import serializers

from sensores.models import Sensor, ReglaControl


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"


class ReglaControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReglaControl
        fields = "__all__"

class LecturaSensorSerializer(serializers.Serializer):
    sensor_codigo = serializers.CharField()
    valor = serializers.DecimalField(max_digits=12, decimal_places=3)
    unidad = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=False)

