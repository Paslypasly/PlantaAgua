from django.db import models
from django.utils import timezone

ESTADOS_PEDIDO = (
    ("RECIBIDO", "1) Recibido"),
    ("PREPARACION", "2) En preparación"),
    ("EN_RUTA", "3) En ruta"),
    ("ENTREGADO", "Entregado"),
    ("FALLIDO", "Fallido/Devuelto"),
)

class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    rut = models.CharField(max_length=12, blank=True)          # opcional
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.rut})" if self.rut else self.nombre


class Pedido(models.Model):
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=15, choices=ESTADOS_PEDIDO, default="RECIBIDO")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observacion = models.TextField(blank=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["planta", "fecha"]),
            models.Index(fields=["estado"]),
        ]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente}"

    def recalc_total(self):
        tot = sum([it.cantidad * it.precio_unit for it in self.items.all()])
        if tot != self.total:
            self.total = tot
            self.save(update_fields=["total"])


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    descripcion = models.CharField(max_length=120)      # simple (ej: "Bidón 20L")
    cantidad = models.PositiveIntegerField()
    precio_unit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.descripcion} x{self.cantidad}"


class PedidoTracking(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="tracking")
    estado = models.CharField(max_length=15, choices=ESTADOS_PEDIDO)
    timestamp = models.DateTimeField(default=timezone.now)
    nota = models.TextField(blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.pedido_id} → {self.estado} @ {self.timestamp:%Y-%m-%d %H:%M}"
