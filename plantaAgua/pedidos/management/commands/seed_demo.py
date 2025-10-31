from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from usuarios.models import Planta, Rol
from pedidos.models import Cliente, Pedido, PedidoItem, PedidoTracking

class Command(BaseCommand):
    help = "Crea datos demo: planta, roles, usuarios, clientes y pedidos"

    def handle(self, *args, **kwargs):
        # Planta
        planta, _ = Planta.objects.get_or_create(
            codigo="SM01",
            defaults={"nombre": "Planta San Miguel", "direccion": "Iquique", "activa": True},
        )

        # Roles
        rol_admin, _ = Rol.objects.get_or_create(nombre="Administrador")
        rol_oper, _ = Rol.objects.get_or_create(nombre="Operador")

        # Usuario demo
        User = get_user_model()
        if not User.objects.filter(username="operador").exists():
            u = User.objects.create_user(username="operador", password="operador123", rol=rol_oper, planta=planta)
            self.stdout.write(self.style.SUCCESS(f"Usuario creado: operador / operador123"))
        else:
            u = User.objects.get(username="operador")

        # Clientes
        c1, _ = Cliente.objects.get_or_create(nombre="Juan Pérez", rut="12.345.678-9", telefono="912345678")
        c2, _ = Cliente.objects.get_or_create(nombre="Ferretería San José", rut="76.111.222-3", telefono="922222222")

        # Pedidos
        p1 = Pedido.objects.create(planta=planta, cliente=c1, estado="RECIBIDO", total=0)
        PedidoItem.objects.create(pedido=p1, descripcion="Bidón 20L", cantidad=3, precio_unit=1500)
        p1.recalc_total()
        PedidoTracking.objects.create(pedido=p1, estado="RECIBIDO", nota="Ingreso por call center")

        p2 = Pedido.objects.create(planta=planta, cliente=c2, estado="PREPARACION", total=0)
        PedidoItem.objects.create(pedido=p2, descripcion="Bidón 20L", cantidad=10, precio_unit=1400)
        p2.recalc_total()
        PedidoTracking.objects.create(pedido=p2, estado="RECIBIDO", nota="Web")
        PedidoTracking.objects.create(pedido=p2, estado="PREPARACION", nota="Armando palet")

        self.stdout.write(self.style.SUCCESS("Datos demo listos."))
