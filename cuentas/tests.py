# cuentas/tests.py
from django.test import TestCase
from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from django.test import override_settings
from django.contrib.auth import get_user_model
from core.decorators import rol_requerido


User = get_user_model()


@rol_requerido("ADMIN")
def vista_solo_admin(request):
    return HttpResponse("OK ADMIN")


urlpatterns = [
    path("solo-admin/", vista_solo_admin, name="solo_admin"),
]


@override_settings(ROOT_URLCONF=__name__)
class RolRequeridoTest(TestCase):
    def setUp(self):
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
        self.client.login(username="admin", password="admin123")
        resp = self.client.get("/solo-admin/")
        self.assertEqual(resp.status_code, 200)

    def test_operario_no_puede_acceder(self):
        self.client.login(username="operario", password="oper123")
        resp = self.client.get("/solo-admin/")
        self.assertEqual(resp.status_code, 403)
