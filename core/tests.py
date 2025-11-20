# core/tests.py
from django.test import TestCase
from clientes.models import SectorEntrega, Cliente


class ClienteModelTest(TestCase):
    def test_crear_cliente_basico_con_dv_automatico(self):
        sector = SectorEntrega.objects.create(nombre="Centro")
        cliente = Cliente.objects.create(
            rut_numero="12345678",  # solo los 8 dígitos
            nombre="Cliente Prueba",
            direccion="Calle Falsa 123",
            sector_entrega=sector,
        )

        # DV correcto de 12345678 es 5
        self.assertEqual(cliente.rut_dv, "5")
        self.assertEqual(cliente.rut_completo, "12345678-5")
        self.assertEqual(str(cliente), "Cliente Prueba (12345678-5)")
