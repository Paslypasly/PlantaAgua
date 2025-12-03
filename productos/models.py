from django.db import models
from core.models import BaseModel


class CategoriaProducto(BaseModel):
    """
    Categoría comercial de productos (e.g. Bidones, Packs, Servicios).
    Hereda de BaseModel, por lo que incluye campos comunes definidos en tu proyecto.
    """
    nombre = models.CharField(max_length=50)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Categoría de producto"
        verbose_name_plural = "Categorías de productos"

    def __str__(self) -> str:
        return self.nombre


class Producto(BaseModel):
    """
    Producto comercial disponible para venta al público.
    Ej: Bidón 20L, Pack 3×20L, etc.
    """
    nombre = models.CharField(max_length=100)

    categoria = models.ForeignKey(
        CategoriaProducto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
        help_text="Categoría comercial del producto (opcional).",
    )

    descripcion = models.TextField(
        blank=True,
        help_text="Descripción breve del producto.",
    )

    presentacion_litros = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Capacidad del envase en litros (ej. 10, 20, 19.5).",
    )

    precio_lista = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio de venta en pesos chilenos.",
    )

    image = models.ImageField(
        upload_to="productos/",
        blank=True,
        null=True,
        help_text="Imagen del producto (opcional).",
    )

    class Meta:
        ordering = ["nombre", "presentacion_litros"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self) -> str:
        return f"{self.nombre} ({self.presentacion_litros}L)"
