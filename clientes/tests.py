# clientes/tests.py
from django.test import TestCase
from clientes.models import Cliente, SectorEntrega


class ClienteRutTest(TestCase):
    def test_dv_se_calcula_automaticamente(self):
        sector = SectorEntrega.objects.create(nombre="Centro")
        cliente = Cliente.objects.create(
            rut_numero="12345678",
            nombre="Prueba",
            direccion="Calle 1",
            sector_entrega=sector,
        )
        # 12345678 -> DV = 5
        self.assertEqual(cliente.rut_dv, "5")
        self.assertEqual(cliente.rut_completo, "12345678-5")
