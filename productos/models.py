# productos/models.py
from django.db import models
from core.models import BaseModel


class CategoriaProducto(BaseModel):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Categoría de producto"
        verbose_name_plural = "Categorías de productos"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


class Producto(BaseModel):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(
        CategoriaProducto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
    )
    presentacion_litros = models.PositiveIntegerField(
        help_text="Capacidad del envase en litros (ej. 10, 20)."
    )
    precio_lista = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre", "presentacion_litros"]

    def __str__(self) -> str:
        return f"{self.nombre} {self.presentacion_litros}L"
