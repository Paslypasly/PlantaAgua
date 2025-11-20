# sensores/tests_iot.py
from django.test import TestCase
from inventario.models import Ubicacion
from planta.models import Estanque
from sensores.models import TipoSensor, Sensor, Actuador, ReglaControl
from sensores.services import registrar_lectura


class IoTBackendTest(TestCase):

    def setUp(self):
        self.ubic = Ubicacion.objects.create(
            codigo="PL1", nombre="Planta", tipo="PLANTA"
        )
        self.estanque = Estanque.objects.create(
            nombre="Crudo", tipo="CRUDO", capacidad_litros=1000, nivel_agua=200
        )
        self.tipo = TipoSensor.objects.create(
            codigo="NIVEL", descripcion="Sensor de nivel"
        )
        self.sensor = Sensor.objects.create(
            tipo=self.tipo,
            estanque=self.estanque,
            codigo="NIVEL_1",
            unidad="cm",
            rango_min=10,
            rango_max=90,
            activo=True
        )
        self.act = Actuador.objects.create(
            tipo="BOMBA",
            nombre="Bomba1"
        )
        self.regla = ReglaControl.objects.create(
            nombre="Alto nivel",
            sensor=self.sensor,
            condicion="MAYOR",
            umbral=80,
            actuador=self.act,
            mensaje="Nivel alto detectado"
        )

    def test_registra_lectura_y_actualiza_estado(self):
        lectura = registrar_lectura("NIVEL_1", 50)
        self.assertIsNotNone(lectura)
        self.sensor.refresh_from_db()
        self.assertEqual(self.sensor.estado, "OK")

    def test_dispara_alerta_por_fuera_de_rango(self):
        registrar_lectura("NIVEL_1", 95)
        self.sensor.refresh_from_db()
        self.assertEqual(self.sensor.estado, "FUERA_RANGO")
        self.assertEqual(self.sensor.alertas.count(), 2)

    def test_dispara_regla_control(self):
        registrar_lectura("NIVEL_1", 100)
        self.act.refresh_from_db()
        self.assertTrue(self.act.estado_on)
