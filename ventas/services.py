from __future__ import annotations

from decimal import Decimal

from django.utils import timezone

from productos.models import Producto
from clientes.models import Cliente, SectorEntrega
from core.utils.rut import calcular_dv
from .models import Pedido, DetallePedido


class CartService:
    """
    Carrito basado en sesión.

    Estructura en session["cart"]:
    {
        "producto_id": {"cantidad": 2},
        "otro_id": {"cantidad": 1},
    }
    """

    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if cart is None:
            cart = {}
            self.session[self.SESSION_KEY] = cart
        self.cart = cart

    def _save(self) -> None:
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def add(self, producto_id: int, cantidad: int = 1, override: bool = False) -> None:
        pid = str(producto_id)
        if pid not in self.cart:
            self.cart[pid] = {"cantidad": 0}

        if override:
            self.cart[pid]["cantidad"] = max(0, cantidad)
        else:
            self.cart[pid]["cantidad"] += cantidad

        if self.cart[pid]["cantidad"] <= 0:
            del self.cart[pid]

        self._save()

    def remove(self, producto_id: int) -> None:
        pid = str(producto_id)
        if pid in self.cart:
            del self.cart[pid]
            self._save()

    def clear(self) -> None:
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def __iter__(self):
        """
        Itera sobre los ítems del carrito devolviendo
        producto, cantidad, precio_unitario, subtotal.
        """
        ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=ids, activo=True)

        for producto in productos:
            data = self.cart.get(str(producto.id), {})
            cantidad = data.get("cantidad", 0)
            precio = producto.precio_lista
            subtotal = cantidad * precio
            yield {
                "producto": producto,
                "cantidad": cantidad,
                "precio_unitario": precio,
                "subtotal": subtotal,
            }

    def total(self) -> Decimal:
        return sum(item["subtotal"] for item in self)


def generar_numero_pedido() -> str:
    """
    Genera un correlativo simple tipo P00001, P00002, ...
    """
    ultimo = Pedido.objects.order_by("-id").first()
    correlativo = 1 if not ultimo else ultimo.id + 1
    return f"P{correlativo:05d}"


def crear_pedido_desde_carrito(cart: CartService, datos_cliente: dict) -> Pedido:
    """
    Convierte el carrito en un Pedido + DetallePedido.

    - Si viene rut_numero, se crea/busca el Cliente por RUT (DV calculado).
    - Si no, se busca por correo (cliente frecuente sin rut).
    """
    nombre = datos_cliente["nombre"]
    correo = datos_cliente["correo"]
    telefono = datos_cliente["telefono"]
    direccion = datos_cliente["direccion"]
    sector_entrega: SectorEntrega = datos_cliente["sector_entrega"]
    comentarios = datos_cliente.get("comentarios", "")
    rut_numero = datos_cliente.get("rut_numero") or ""
    forma_pago = datos_cliente.get("forma_pago", "EFECTIVO")

    if rut_numero:
        rut_numero_str = str(rut_numero)
        cliente, created = Cliente.objects.get_or_create(
            rut_numero=rut_numero_str,
            defaults={
                "rut_dv": calcular_dv(rut_numero_str),
                "nombre": nombre,
                "correo": correo,
                "telefono": telefono,
                "direccion": direccion,
                "sector_entrega": sector_entrega,
            },
        )
        if not created:
            cliente.nombre = nombre
            cliente.correo = correo
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.sector_entrega = sector_entrega
            cliente.save()
    else:
        cliente, _ = Cliente.objects.get_or_create(
            correo=correo,
            defaults={
                "nombre": nombre,
                "telefono": telefono,
                "direccion": direccion,
                "sector_entrega": sector_entrega,
            },
        )

    pedido = Pedido.objects.create(
        numero=generar_numero_pedido(),
        cliente=cliente,
        sector_entrega=sector_entrega,
        fecha=timezone.now().date(),
        origen="WEB",
        comentarios_cliente=comentarios,
        forma_pago=forma_pago,
    )

    for item in cart:
        DetallePedido.objects.create(
            pedido=pedido,
            producto=item["producto"],
            cantidad=item["cantidad"],
            precio_unitario=item["precio_unitario"],
        )

    pedido.calcular_total()
    pedido.save()
    return pedido
