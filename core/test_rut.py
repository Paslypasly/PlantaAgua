# core/tests_rut.py
from django.test import TestCase
from core.utils import rut as rut_utils


class RutUtilsTest(TestCase):
    def test_calcular_dv_conocidos(self):
        # Casos conocidos
        self.assertEqual(rut_utils.calcular_dv("11111111"), "1")
        self.assertEqual(rut_utils.calcular_dv("12345678"), "5")
        self.assertEqual(rut_utils.calcular_dv("76086428"), "5")  # Ejemplo real

    def test_validar_rut_completo(self):
        self.assertTrue(rut_utils.validar_rut_completo("11111111", "1"))
        self.assertFalse(rut_utils.validar_rut_completo("11111111", "9"))
