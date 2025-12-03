from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from core.decorators import rol_requerido  # tu decorador real

User = get_user_model()


# Vista mínima solo para probar el decorador
@login_required
@rol_requerido("ADMIN")
def vista_solo_admin(request):
    return HttpResponse("Solo admin")


class RolRequeridoTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.admin = User.objects.create_user(
            username="admin",
            password="admin123",
            rol="ADMIN",
        )

        self.operario = User.objects.create_user(
            username="operario",
            password="oper123",
            rol="OPERARIO",
        )

    def test_admin_puede_acceder(self):
        """
        Un usuario con rol ADMIN debe poder acceder
        y la vista debe responder 200 OK.
        """
        request = self.factory.get("/solo-admin/")
        request.user = self.admin

        response = vista_solo_admin(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Solo admin")

    def test_operario_no_puede_acceder(self):
        """
        Un usuario con rol OPERARIO debe generar PermissionDenied
        al intentar acceder a la vista solo-admin.
        """
        request = self.factory.get("/solo-admin/")
        request.user = self.operario

        with self.assertRaises(PermissionDenied):
            vista_solo_admin(request)
