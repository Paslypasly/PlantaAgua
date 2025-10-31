from django.db import models
from django.utils import timezone

class RutaDistribucion(models.Model):
    ESTADOS = (("planificada","Planificada"),("en_ruta","En ruta"),("cerrada","Cerrada"))
    planta = models.ForeignKey("usuarios.Planta", on_delete=models.PROTECT)
    fecha = models.DateField(default=timezone.now)
    chofer = models.CharField(max_length=100)
    vehiculo = models.CharField(max_length=60)
    estado = models.CharField(max_length=15, choices=ESTADOS, default="planificada")

    def __str__(self):
        return f"Ruta {self.fecha} [{self.planta.codigo}] - {self.chofer}"


class RutaParada(models.Model):
    ruta = models.ForeignKey(RutaDistribucion, on_delete=models.CASCADE, related_name="paradas")
    pedido = models.ForeignKey("pedidos.Pedido", on_delete=models.PROTECT)
    orden = models.PositiveIntegerField()
    eta = models.DateTimeField(null=True, blank=True)
    llegada = models.DateTimeField(null=True, blank=True)
    salida = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=15, default="pendiente")  # pendiente/atendida/fallida

    class Meta:
        ordering = ["orden"]
        unique_together = [("ruta", "pedido")]

    def __str__(self):
        return f"Parada {self.orden} → Pedido #{self.pedido_id}"
