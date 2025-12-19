# ventas/services.py
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Iterable, Iterator, Dict

from django.db import transaction
from django.utils import timezone

from clientes.models import Cliente, SectorEntrega
from productos.models import Producto
from core.utils.rut import calcular_dv, validar_rut_completo

from .models import Pedido, DetallePedido
from produccion.models import LoteProduccion
from datetime import date
from produccion.models import LoteProduccion
from django.utils.timezone import localdate


# =========================
#  CARRITO POR SESIÓN
# =========================
class CartService:
    """
    Carrito basado en session (no requiere modelo CarritoItem).
    Guarda: {producto_id: {"cantidad": int}}
    """
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if cart is None:
            cart = self.session[self.SESSION_KEY] = {}
        self.cart: Dict[str, Dict[str, Any]] = cart

    def add(self, producto_id: int, cantidad: int = 1):
        pid = str(producto_id)
        if pid not in self.cart:
            self.cart[pid] = {"cantidad": 0}
        self.cart[pid]["cantidad"] += int(cantidad)
        if self.cart[pid]["cantidad"] < 1:
            self.cart[pid]["cantidad"] = 1
        self.save()

    def set(self, producto_id: int, cantidad: int):
        pid = str(producto_id)
        self.cart[pid] = {"cantidad": max(1, int(cantidad))}
        self.save()

    def remove(self, producto_id: int):
        pid = str(producto_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.cart = self.session[self.SESSION_KEY]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self) -> Iterator["CartLine"]:
        """
        Devuelve líneas ricas (producto, cantidad, precio_unitario, subtotal).
        """
        ids = [int(pid) for pid in self.cart.keys()] if self.cart else []
        productos = Producto.objects.filter(id__in=ids)
        productos_map = {p.id: p for p in productos}

        for pid_str, data in self.cart.items():
            pid = int(pid_str)
            producto = productos_map.get(pid)
            if not producto:
                continue

            cantidad = int(data.get("cantidad", 1))
            precio = Decimal(str(getattr(producto, "precio_lista", 0)))

            yield CartLine(
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio,
            )

    def total(self) -> Decimal:
        return sum((line.subtotal for line in self), Decimal("0"))


@dataclass
class CartLine:
    producto: Producto
    cantidad: int
    precio_unitario: Decimal

    @property
    def subtotal(self) -> Decimal:
        return Decimal(self.cantidad) * Decimal(self.precio_unitario)


# =========================
#  CHECKOUT (con/sin RUT)
# =========================
from core.utils.rut import calcular_dv, validar_rut_completo

def _get_or_create_cliente_publico(data):
    """
    Crea o reutiliza un cliente público (checkout sin usuario).
    Maneja casos con o sin RUT.
    """
    from clientes.models import Cliente, SectorEntrega

    nombre = data.get("nombre", "").strip()
    correo = data.get("correo", "").strip()
    telefono = data.get("telefono", "").strip()
    direccion = data.get("direccion", "").strip()
    sector = data.get("sector_entrega")
    rut_num = (data.get("rut_numero") or "").strip()

    # --- CASO CON RUT -------------------------------------------------------
    if rut_num:
        rut_num = str(rut_num).strip()  # <-- fuerza tipo string
        dv = calcular_dv(rut_num)

        if not validar_rut_completo(rut_num, dv):
            raise ValueError("RUT inválido.")

        cliente, _ = Cliente.objects.get_or_create(
            rut=rut_num,      # texto
            dv=str(dv),       # texto
            defaults={
                "nombre": nombre,
                "direccion": direccion,
                "email": correo,
                "telefono": telefono,
                "sector_entrega": sector,
                "activo": True,
            },
        )
        return cliente

    # --- CASO SIN RUT -------------------------------------------------------
    cliente, _ = Cliente.objects.get_or_create(
        rut="0",
        dv="0",
        defaults={
            "nombre": "Cliente Web (Sin RUT)",
            "direccion": direccion,
            "email": correo,
            "telefono": telefono,
            "sector_entrega": sector,
            "activo": True,
        },
    )

    # Si el cliente ya existía, actualiza sus datos
    changed = False
    if cliente.email != correo:
        cliente.email = correo
        changed = True
    if cliente.telefono != telefono:
        cliente.telefono = telefono
        changed = True
    if cliente.direccion != direccion:
        cliente.direccion = direccion
        changed = True
    if cliente.sector_entrega != sector:
        cliente.sector_entrega = sector
        changed = True

    if changed:
        cliente.save(update_fields=["email", "telefono", "direccion", "sector_entrega"])

    return cliente



@transaction.atomic
def crear_pedido_desde_carrito(cart: Iterable[Any], cleaned_data: dict) -> Pedido:
    """
    Crea un Pedido y sus Detalles desde el carrito de compras.
    También genera automáticamente un Lote de Producción asociado.
    """
    # 1. Crear o reutilizar cliente
    cliente = _get_or_create_cliente_publico(cleaned_data)

    sector: SectorEntrega = cleaned_data["sector_entrega"]
    forma_pago = cleaned_data.get("forma_pago", "EFECTIVO")
    comentarios = (cleaned_data.get("comentarios") or "").strip()

    # 2. Generar número de pedido único
    numero = timezone.now().strftime("WEB%Y%m%d%H%M%S")

    # 3. Crear pedido base
    pedido = Pedido.objects.create(
        numero=numero,
        cliente=cliente,
        sector_entrega=sector,
        fecha=timezone.localdate(),
        estado="PENDIENTE",
        total=0,
        origen="WEB",
        comentarios_cliente=comentarios,
        forma_pago=forma_pago,
    )

    # 4. Crear detalles
    total = Decimal("0")
    litros_totales = 0

    for line in cart:  # line es CartLine
        DetallePedido.objects.create(
            pedido=pedido,
            producto=line.producto,
            cantidad=line.cantidad,
            precio_unitario=line.precio_unitario,
        )
        total += line.subtotal

        # Estima litros si el producto tiene campo volumen_litros
        litros_totales += (
            getattr(line.producto, "volumen_litros", 20) * line.cantidad
        )

    pedido.total = total
    pedido.save(update_fields=["total"])

    # 5. Crear lote de producción automáticamente
    try:
        from produccion.models import LoteProduccion
        from django.utils.timezone import now, localdate

        LoteProduccion.objects.create(
            fecha=localdate(),
            hora_inicio=now().time(),
            hora_fin=(now() + timezone.timedelta(minutes=15)).time(),
            litros=litros_totales,
            estanque=None,  # asignar si tienes un estanque predeterminado
            estado="PENDIENTE",
            observaciones=f"Lote generado automáticamente desde pedido {pedido.numero}",
        )
        print(f"✅ Lote de producción creado ({litros_totales} L) desde pedido {pedido.numero}")

    except Exception as e:
        print(f"⚠️ Error creando lote de producción: {e}")

    # 6. DEVOLVER pedido creado
    return pedido



def generar_plan_produccion_desde_pedido(pedido):
    """
    Genera automáticamente un plan de producción cuando se registra un pedido web.
    """
    try:
        LoteProduccion.objects.create(
            fecha=date.today(),
            litros=float(pedido.total),  # puedes ajustar si 1 peso ≠ 1 litro
            estado="PENDIENTE",
            observaciones=f"Pedido web {pedido.numero} generado automáticamente.",
        )
    except Exception as e:
        print(f"⚠️ Error creando lote de producción: {e}")