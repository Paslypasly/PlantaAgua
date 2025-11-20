# produccion/views.py
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView

from core.mixins import RolRequiredMixin
from .models import LoteProduccion


class PlanProduccionDiariaView(RolRequiredMixin, TemplateView):
    """
    Vista tipo resumen de producción.
    De momento muestra la fecha de hoy y los últimos lotes.
    """
    template_name = "produccion/plan_produccion_diaria.html"
    rol_requerido = None  # cualquier usuario autenticado

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["hoy"] = timezone.localdate()
        # Ordenamos por id para no depender de campos que quizá no existan
        ctx["lotes"] = LoteProduccion.objects.all().order_by("-id")[:20]
        return ctx


class OrdenesProduccionListView(RolRequiredMixin, ListView):
    """
    Listado general de órdenes / lotes de producción.
    """
    model = LoteProduccion
    template_name = "produccion/ordenes_produccion_list.html"
    context_object_name = "lotes"
    paginate_by = 20
    rol_requerido = None  # luego se puede restringir a OPERARIO/GERENTE

    def get_queryset(self):
        return LoteProduccion.objects.all().order_by("-id")


class OrdenProduccionDetalleView(RolRequiredMixin, DetailView):
    """
    Detalle de un lote / orden de producción.
    """
    model = LoteProduccion
    template_name = "produccion/orden_produccion_detalle.html"
    context_object_name = "lote"
    rol_requerido = None


class ConsumoInsumosView(RolRequiredMixin, TemplateView):
    """
    Vista de consumo de insumos asociado a la producción.
    Por ahora placeholder; más adelante se cruza con inventario.
    """
    template_name = "produccion/consumo_insumos.html"
    rol_requerido = None
