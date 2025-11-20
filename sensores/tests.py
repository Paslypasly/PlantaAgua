# sensores/tests.py
from django.test import TestCase
from django.utils import timezone
from inventario.models import Ubicacion
from planta.models import Estanque
from sensores.models import TipoSensor, Sensor, LecturaSensor


class SensorModelTest(TestCase):
    def test_ultima_lectura(self):
        ubic = Ubicacion.objects.create(
            codigo="PLANTA1",
            nombre="Planta 1",
            tipo="PLANTA"
        )
        estanque = Estanque.objects.create(
            nombre="Estanque Crudo",
            tipo="CRUDO",
            capacidad_litros=1000,
            nivel_agua=500,
            ubicacion=ubic,
        )
        tipo = TipoSensor.objects.create(
            codigo="NIVEL",
            descripcion="Sensor de nivel"
        )
        sensor = Sensor.objects.create(
            tipo=tipo,
            estanque=estanque,
            codigo="SENS_NIVEL_1",
            unidad="cm",
        )
        LecturaSensor.objects.create(
            sensor=sensor,
            fecha_hora=timezone.now(),
            valor=100
        )

        self.assertIsNotNone(sensor.ultima_lectura())
