from django.test import TestCase

# Create your tests here.
# core/tests.py
from django.test import TestCase
from clientes.models import SectorEntrega, Cliente


class ClienteModelTest(TestCase):
    def test_crear_cliente_basico(self):
        sector = SectorEntrega.objects.create(nombre="Centro")
        cliente = Cliente.objects.create(
            rut_numero="12345678",
            rut_dv="9",
            nombre="Cliente Prueba",
            direccion="Calle Falsa 123",
            sector_entrega=sector,
        )
        self.assertEqual(str(cliente), "Cliente Prueba (12345678-9)")
