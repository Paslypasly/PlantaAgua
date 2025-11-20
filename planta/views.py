# planta/views.py
from django.views.generic import TemplateView, ListView

from core.mixins import RolRequiredMixin
from .models import Estanque, EventoPlanta
from produccion.models import LoteProduccion


class EstadoEstanquesView(RolRequiredMixin, TemplateView):
    """
    Vista de estado de estanques.
    Cualquier usuario autenticado puede verla (rol_requerido = None).
    """
    template_name = "planta/estado_estanques.html"
    rol_requerido = None  # todos los usuarios logueados

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        estanques = Estanque.objects.all().order_by("nombre")

        total_capacidad = sum(e.capacidad_litros for e in estanques)
        total_actual = sum(float(e.nivel_agua or 0) for e in estanques)

        ctx["estanques"] = estanques
        ctx["total_capacidad"] = total_capacidad
        ctx["total_actual"] = total_actual
        ctx["porcentaje_global"] = (
            (total_actual / total_capacidad * 100) if total_capacidad > 0 else 0
        )

        return ctx


class EventosPlantaView(RolRequiredMixin, ListView):
    """
    Lista de eventos de planta (paros, mantenciones, alertas manuales).
    Cualquier usuario autenticado puede verla.
    """
    model = EventoPlanta
    template_name = "planta/eventos_planta.html"
    context_object_name = "eventos"
    paginate_by = 20
    rol_requerido = None  # todos los usuarios logueados

    def get_queryset(self):
        return (
            EventoPlanta.objects.all()
            .select_related("estanque")
            .order_by("-fecha_hora")
        )


class ControlPlantaView(RolRequiredMixin, TemplateView):
    """
    Panel de control para el OPERARIO:
    - Ver estado de estanques
    - Ver bombas y su estado (más adelante)
    - Ver últimos lotes de producción
    """
    template_name = "planta/control_planta.html"
    rol_requerido = "OPERARIO"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["estanques"] = Estanque.objects.all().order_by("nombre")
        ctx["ultimos_lotes"] = (
            LoteProduccion.objects.all()
            .order_by("-fecha_creacion")[:5]
        )

        return ctx
