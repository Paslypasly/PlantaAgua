# productos/views.py
from django.views.generic import ListView, DetailView
from .models import Producto


class CatalogoPublicoView(ListView):
    """
    Catálogo público de productos visibles para cualquier usuario.
    """
    model = Producto
    template_name = "cliente_publico/catalogo.html"
    context_object_name = "productos"

    def get_queryset(self):
        # Si más adelante quieres filtrar por activos, descomentas esto:
        # return Producto.objects.filter(activo=True).order_by("nombre", "presentacion_litros")
        return Producto.objects.all().order_by("nombre", "presentacion_litros")


class ProductoDetallePublicoView(DetailView):
    """
    Vista de detalle pública de un producto.
    """
    model = Producto
    template_name = "cliente_publico/detalle_producto.html"
    context_object_name = "producto"
