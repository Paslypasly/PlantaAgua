# productos/tests.py
from django.test import TestCase
from .models import CategoriaProducto, Producto


class ProductoModelTest(TestCase):
    def test_str_producto(self):
        categoria = CategoriaProducto.objects.create(nombre="Bidones")
        producto = Producto.objects.create(
            nombre="Agua purificada",
            categoria=categoria,
            presentacion_litros=20,
            precio_lista=3000,
        )
        self.assertIn("20L", str(producto))
