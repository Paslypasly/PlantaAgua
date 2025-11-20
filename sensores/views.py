# sensores/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib import messages

from core.mixins import RolRequiredMixin
from .models import Sensor, LecturaSensor, Alerta, Actuador, ReglaControl


# ============================================================
# DASHBOARD GENERAL PLANTA + IOT
# ============================================================

class DashboardPlantaView(LoginRequiredMixin, TemplateView):
    """
    Vista principal de planta + sensores.
    Operario: la usa todo el día.
    Gerente: la ve en modo lectura.
    """
    template_name = "sensores/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_sensores = Sensor.objects.count()
        sensores_activos = Sensor.objects.filter(activo=True).count()
        alertas_abiertas = Alerta.objects.filter(estado="ABIERTA").count()

        ultimas_lecturas = (
            LecturaSensor.objects
            .select_related("sensor")
            .order_by("-fecha_hora")[:10]
        )

        context.update({
            "total_sensores": total_sensores,
            "sensores_activos": sensores_activos,
            "alertas_abiertas": alertas_abiertas,
            "ultimas_lecturas": ultimas_lecturas,
        })
        return context


# ============================================================
# SENSORES
# ============================================================

class SensorListView(LoginRequiredMixin, ListView):
    model = Sensor
    template_name = "sensores/lista_sensores.html"
    context_object_name = "sensores"
    paginate_by = 20


class SensorDetailView(LoginRequiredMixin, DetailView):
    model = Sensor
    template_name = "sensores/detalle_sensor.html"
    context_object_name = "sensor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sensor = self.object
        lecturas_recientes = (
            LecturaSensor.objects
            .filter(sensor=sensor)
            .order_by("-fecha_hora")[:20]
        )
        alertas_sensor = (
            Alerta.objects
            .filter(sensor=sensor)
            .order_by("-created_at")[:10]
        )
        context.update({
            "lecturas_recientes": lecturas_recientes,
            "alertas_sensor": alertas_sensor,
        })
        return context


# ============================================================
# ALERTAS
# ============================================================

class AlertaListView(LoginRequiredMixin, ListView):
    model = Alerta
    template_name = "sensores/alertas_list.html"
    context_object_name = "alertas"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related("sensor")
        estado = self.request.GET.get("estado")
        if estado:
            qs = qs.filter(estado=estado)
        return qs.order_by("-created_at")


class AlertaDetailView(LoginRequiredMixin, DetailView):
    model = Alerta
    template_name = "sensores/alerta_detalle.html"
    context_object_name = "alerta"


# ============================================================
# REGLAS DE CONTROL (solo OPERARIO / ADMIN)
# ============================================================

class ReglaListView(LoginRequiredMixin, ListView):
    model = ReglaControl
    template_name = "sensores/reglas_list.html"
    context_object_name = "reglas"
    paginate_by = 20

    def get_queryset(self):
        return (
            ReglaControl.objects
            .select_related("sensor", "actuador")
            .order_by("-prioridad", "sensor__nombre")
        )


class ReglaCreateView(RolRequiredMixin, CreateView):
    model = ReglaControl
    fields = ["nombre", "sensor", "actuador", "condicion", "umbral_min",
              "umbral_max", "prioridad", "activo"]
    template_name = "sensores/regla_form.html"
    success_url = reverse_lazy("reglas_list")
    rol_requerido = "OPERARIO"  # también podría ser Usuario.Rol.OPERARIO

    def form_valid(self, form):
        messages.success(self.request, "Regla de control creada correctamente.")
        return super().form_valid(form)


class ReglaUpdateView(RolRequiredMixin, UpdateView):
    model = ReglaControl
    fields = ["nombre", "sensor", "actuador", "condicion", "umbral_min",
              "umbral_max", "prioridad", "activo"]
    template_name = "sensores/regla_form.html"
    success_url = reverse_lazy("reglas_list")
    rol_requerido = "OPERARIO"

    def form_valid(self, form):
        messages.success(self.request, "Regla de control actualizada correctamente.")
        return super().form_valid(form)


# ============================================================
# HISTORIAL DE LECTURAS
# ============================================================

class LecturasHistorialView(LoginRequiredMixin, ListView):
    model = LecturaSensor
    template_name = "sensores/lecturas_historial.html"
    context_object_name = "lecturas"
    paginate_by = 50

    def get_queryset(self):
        qs = (
            LecturaSensor.objects
            .select_related("sensor")
            .order_by("-fecha_hora")
        )
        sensor_id = self.request.GET.get("sensor")
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)
        return qs


# ============================================================
# ACTUADORES
# ============================================================

class ActuadorListView(LoginRequiredMixin, ListView):
    model = Actuador
    template_name = "sensores/actuadores_list.html"
    context_object_name = "actuadores"
    paginate_by = 20


class ActuadorDetailView(LoginRequiredMixin, DetailView):
    model = Actuador
    template_name = "sensores/actuador_detalle.html"
    context_object_name = "actuador"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reglas = ReglaControl.objects.filter(actuador=self.object)
        context["reglas"] = reglas
        return context
