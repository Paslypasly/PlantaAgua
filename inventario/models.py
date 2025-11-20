# inventario/models.py
from django.db import models
from core.models import BaseModel


class Ubicacion(BaseModel):
    TIPO_CHOICES = [
        ("BODEGA", "Bodega"),
        ("PLANTA", "Planta"),
        ("PROCESO", "Proceso"),
        ("ESTANQUE", "Estanque"),
        ("DESPACHO", "Despacho"),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}"


class Insumo(BaseModel):
    TIPO_CHOICES = [
        ("FILTRO", "Filtro"),
        ("QUIMICO", "Químico"),
        ("ENVASE", "Envase"),
        ("OTRO", "Otro"),
    ]

    nombre = models.CharField(max_length=100)
    tipo_insumo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    unidad = models.CharField(max_length=20, help_text="Ej. unidad, kg, litro.")
    stock_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Stock mínimo recomendado."
    )

    def __str__(self) -> str:
        return self.nombre


class StockInsumo(BaseModel):
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.CASCADE,
        related_name="stocks_insumo"
    )
    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        related_name="stocks"
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("ubicacion", "insumo")

    def __str__(self) -> str:
        return f"{self.insumo} @ {self.ubicacion}: {self.cantidad}"


class StockProducto(BaseModel):
    """
    Stock de productos terminados (bidones) por ubicación.
    Corresponde al StockProducto del MER.
    """
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="stocks"
    )
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.CASCADE,
        related_name="stocks_producto"
    )
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("producto", "ubicacion")

    def __str__(self) -> str:
        return f"{self.producto} @ {self.ubicacion}: {self.cantidad}"


class MovimientoInventario(BaseModel):
    TIPO_MOV_CHOICES = [
        ("ENTRADA", "Entrada"),
        ("SALIDA", "Salida"),
        ("AJUSTE", "Ajuste"),
    ]

    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.PROTECT,
        related_name="movimientos"
    )
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name="movimientos"
    )
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOV_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    comentario = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"{self.tipo_movimiento} {self.cantidad} de {self.insumo}"
