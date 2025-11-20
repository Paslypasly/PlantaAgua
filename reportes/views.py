# reportes/views.py
from django.views.generic import TemplateView
from core.mixins import RolRequiredMixin
from django.utils import timezone
from ventas.models import Pedido
from inventario.models import Insumo
from produccion.models import LoteProduccion


class ReporteResumenDiarioView(RolRequiredMixin, TemplateView):
    template_name = "reportes/resumen_diario.html"
    roles_permitidos = ["ADMIN", "GERENTE"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.now().date()

        pedidos_hoy = Pedido.objects.filter(fecha__date=hoy).count()
        produccion_hoy = LoteProduccion.objects.filter(fecha__date=hoy).count()
        insumos_bajos = Insumo.objects.filter(stock_actual__lt=10).count()  # umbral ejemplo

        ctx.update({
            "pedidos_hoy": pedidos_hoy,
            "produccion_hoy": produccion_hoy,
            "insumos_bajos": insumos_bajos,
            "fecha": hoy,
        })
        return ctx
