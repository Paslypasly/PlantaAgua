from django.views.generic import ListView, DetailView

from .models import Producto


class CatalogoPublicoView(ListView):
    """
    Vista de catálogo público para clientes (no requiere login).
    """
    model = Producto
    template_name = "cliente_publico/catalogo.html"
    context_object_name = "productos"

    def get_queryset(self):
        # Solo productos activos, ordenados por nombre y presentación
        qs = Producto.objects.all()
        if hasattr(Producto, "activo"):
            qs = qs.filter(activo=True)
        return qs.order_by("nombre", "presentacion_litros")


class ProductoDetallePublicoView(DetailView):
    """
    Detalle de producto público para clientes.
    """
    model = Producto
    template_name = "cliente_publico/detalle_producto.html"
    context_object_name = "producto"
