# ventas/views.py
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, FormView
from django.views.decorators.http import require_POST

from core.mixins import RolRequiredMixin
from .models import Pedido
from .services import CartService, crear_pedido_desde_carrito
from .forms import CheckoutPublicoForm

# Auditoría y notificaciones
from auditoria.services import registrar_evento
from notificaciones.services import crear_notificacion_para_roles


# =====================================================
# VISTAS INTERNAS (Panel Administrativo)
# =====================================================

class PedidoListView(RolRequiredMixin, ListView):
    model = Pedido
    template_name = "ventas/pedido_list.html"
    context_object_name = "pedidos"
    roles_permitidos = ["ADMIN", "OPERARIO", "GERENTE"]


class PedidoCreateView(RolRequiredMixin, CreateView):
    model = Pedido
    fields = ["cliente", "sector_entrega", "fecha", "estado", "total", "forma_pago"]
    template_name = "ventas/pedido_form.html"
    success_url = reverse_lazy("ventas:ventas_pedidos")
    roles_permitidos = ["ADMIN", "OPERARIO"]

    def form_valid(self, form):
        response = super().form_valid(form)
        pedido: Pedido = self.object

        registrar_evento(
            modulo="VENTAS",
            descripcion=f"Pedido interno {pedido.numero} creado por {self.request.user.username}",
            severidad="INFO",
        )
        return response


# =====================================================
# VISTAS PÚBLICAS – CARRITO (SESION)
# =====================================================

class CarritoView(TemplateView):
    template_name = "ventas/carrito.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = CartService(self.request)
        ctx["items"] = list(cart)
        ctx["total"] = cart.total()
        return ctx


class CarritoAgregarView(View):
    def post(self, request, producto_id: int):
        cart = CartService(request)

        try:
            cantidad = int(request.POST.get("cantidad", "1"))
        except ValueError:
            cantidad = 1

        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser mayor a cero.")
            return redirect("productos:catalogo_publico")

        cart.add(producto_id, cantidad=cantidad)
        messages.success(request, "Producto agregado al carrito.")
        return redirect("productos:catalogo_publico")


from django.views.decorators.http import require_POST

@require_POST
def carrito_actualizar(request, producto_id):
    try:
        cantidad = int(request.POST.get("cantidad", "1"))
    except ValueError:
        cantidad = 1

    if cantidad < 1:
        cantidad = 1

    cart = CartService(request)
    cart.set(producto_id, cantidad)
    return redirect("ventas:carrito")



class CarritoEliminarView(View):
    def post(self, request, producto_id: int):
        cart = CartService(request)
        cart.remove(producto_id)
        messages.info(request, "Producto eliminado del carrito.")
        return redirect("ventas:carrito")


class CheckoutPublicoView(FormView):
    template_name = "ventas/checkout_publico.html"
    form_class = CheckoutPublicoForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = CartService(self.request)
        ctx["items"] = list(cart)
        ctx["total"] = cart.total()
        return ctx

    def form_valid(self, form):
        cart = CartService(self.request)

        if cart.total() == 0:
            form.add_error(None, "El carrito está vacío.")
            return self.form_invalid(form)

        pedido = crear_pedido_desde_carrito(cart, form.cleaned_data)
        cart.clear()

        registrar_evento(
            modulo="VENTAS",
            descripcion=(
                f"Nuevo pedido web {pedido.numero} para cliente {pedido.cliente.nombre}. "
                f"Total ${pedido.total}."
            ),
            severidad="INFO",
        )

        crear_notificacion_para_roles(
            roles=["ADMIN", "OPERARIO"],
            tipo="SISTEMA",
            titulo=f"Nuevo pedido web {pedido.numero}",
            mensaje=(
                f"Se registró un nuevo pedido WEB de {pedido.cliente.nombre} "
                f"por un total de ${pedido.total}."
            ),
        )

        messages.success(
            self.request,
            f"Tu pedido {pedido.numero} fue registrado correctamente. "
            "Nos contactaremos contigo para coordinar la entrega."
        )
        return redirect("productos:catalogo_publico")
