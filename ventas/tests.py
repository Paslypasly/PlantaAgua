# ventas/tests.py
from datetime import date
from django.test import TestCase
from clientes.models import SectorEntrega, Cliente
from productos.models import CategoriaProducto, Producto
from ventas.models import Pedido, DetallePedido


class PedidoModelTest(TestCase):
    def test_calculo_total(self):
        sector = SectorEntrega.objects.create(nombre="Centro")
        cliente = Cliente.objects.create(
            rut_numero="12345678",
            rut_dv="9",
            nombre="Cliente Prueba",
            direccion="Calle Falsa 123",
            sector_entrega=sector,
        )
        pedido = Pedido.objects.create(
            numero="P0001",
            cliente=cliente,
            sector_entrega=sector,
            fecha=date.today(),
        )
        cat = CategoriaProducto.objects.create(nombre="Bidones")
        prod = Producto.objects.create(
            nombre="Bidón 20L",
            categoria=cat,
            presentacion_litros=20,
            precio_lista=2000,
        )
        DetallePedido.objects.create(
            pedido=pedido,
            producto=prod,
            cantidad=3,
            precio_unitario=2500,
        )

        total = pedido.calcular_total()
        self.assertEqual(total, 3 * 2500)
