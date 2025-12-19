from django.db import models
from core.models import BaseModel


class Pedido(BaseModel):
    """
    Modelo principal de ventas/pedidos.
    Registra el encabezado de cada venta (cliente, forma de pago, total, etc.).
    """

    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("EN_RUTA", "En ruta"),
        ("ENTREGADO", "Entregado"),
        ("CANCELADO", "Cancelado"),
    ]

    ORIGEN_CHOICES = [
        ("INTERNO", "Interno"),
        ("WEB", "Web público"),
    ]

    FORMA_PAGO_CHOICES = [
        ("EFECTIVO", "Efectivo"),
        ("TRANSFERENCIA", "Transferencia bancaria"),
    ]

    numero = models.CharField(max_length=20, unique=True)

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="pedidos",
    )

    sector_entrega = models.ForeignKey(
        "clientes.SectorEntrega",
        on_delete=models.PROTECT,
        related_name="pedidos",
    )

    fecha = models.DateField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="PENDIENTE",
    )

    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    origen = models.CharField(
        max_length=20,
        choices=ORIGEN_CHOICES,
        default="INTERNO",
    )

    comentarios_cliente = models.TextField(blank=True)

    forma_pago = models.CharField(
        max_length=20,
        choices=FORMA_PAGO_CHOICES,
        default="EFECTIVO",
    )

    def __str__(self) -> str:
        return f"Pedido {self.numero}"

    def calcular_total(self) -> float:
        """
        Calcula y actualiza el total del pedido en base a sus detalles.
        Si un detalle tiene valores nulos, los ignora.
        """
        total = sum(det.subtotal for det in self.detalles.all() if det.subtotal is not None)
        self.total = total
        self.save(update_fields=["total"])
        return total


class DetallePedido(BaseModel):
    """
    Detalle de cada producto asociado a un pedido.
    """

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.PROTECT,
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def subtotal(self) -> float:
        """
        Calcula el subtotal del detalle.
        Evita errores si cantidad o precio son None.
        """
        cantidad = self.cantidad or 0
        precio = self.precio_unitario or 0
        return cantidad * precio

    def save(self, *args, **kwargs):
        """
        Guarda el detalle y actualiza automáticamente el total del pedido.
        """
        super().save(*args, **kwargs)
        # Recalcular el total del pedido al guardar un detalle
        if self.pedido_id:
            self.pedido.calcular_total()

    def delete(self, *args, **kwargs):
        """
        Recalcula el total del pedido si se elimina un detalle.
        """
        pedido = self.pedido
        super().delete(*args, **kwargs)
        if pedido:
            pedido.calcular_total()

    def __str__(self) -> str:
        return f"{self.cantidad} x {self.producto} (Pedido {self.pedido.numero})"
