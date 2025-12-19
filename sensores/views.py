# sensores/views.py
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
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
from .services import forzar_actuador, activar_sensor, actualizar_umbrales


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
        alertas_abiertas = Alerta.objects.filter(atendida=False).count()

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
            qs = qs.filter(atendida=(estado == "ATENDIDA"))
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
            .order_by("sensor__codigo")
        )


class ReglaCreateView(RolRequiredMixin, CreateView):
    model = ReglaControl
    fields = ["nombre", "sensor", "actuador", "condicion", "umbral", "mensaje"]
    template_name = "sensores/regla_form.html"
    success_url = reverse_lazy("reglas_list")
    rol_requerido = "OPERARIO"

    def form_valid(self, form):
        messages.success(self.request, "Regla de control creada correctamente.")
        return super().form_valid(form)


class ReglaUpdateView(RolRequiredMixin, UpdateView):
    model = ReglaControl
    fields = ["nombre", "sensor", "actuador", "condicion", "umbral", "mensaje"]
    template_name = "sensores/regla_form.html"
    success_url = reverse_lazy("reglas_list")
    rol_requerido = "OPERARIO"

    def form_valid(self, form):
        messages.success(self.request, "Regla de control actualizada correctamente.")
        return super().form_valid(form)


# ============================================================
# HISTORIAL DE LECTURAS (ADMIN / TÉCNICO)
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


# ============================================================
# === BLOQUE EXCLUSIVO PARA ADMINISTRADOR ====================
# ============================================================

def es_admin(user):
    return user.is_superuser or user.groups.filter(name="ADMIN").exists()


@user_passes_test(es_admin)
def historico_sensores(request):
    """Histórico avanzado de lecturas con filtros y exportación."""
    sensores = Sensor.objects.all()
    sensor_id = request.GET.get("sensor")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    lecturas = LecturaSensor.objects.all().select_related("sensor")

    if sensor_id:
        lecturas = lecturas.filter(sensor_id=sensor_id)
    if desde and hasta:
        lecturas = lecturas.filter(fecha_hora__range=[desde, hasta])

    return render(request, "sensores/historico_admin.html", {
        "sensores": sensores,
        "lecturas": lecturas.order_by("-fecha_hora")[:500],
    })


@user_passes_test(es_admin)
def control_actuadores(request):
    """Panel administrativo para forzar actuadores."""
    actuadores = Actuador.objects.all()
    if request.method == "POST":
        act_id = request.POST.get("actuador_id")
        estado = request.POST.get("estado") == "1"
        forzar_actuador(act_id, estado, request.user)
        messages.success(request, f"Actuador actualizado correctamente.")
        return redirect("control_actuadores")

    return render(request, "sensores/control_actuadores.html", {
        "actuadores": actuadores,
    })


@user_passes_test(es_admin)
def configurar_umbrales(request):
    """Panel de ajuste de umbrales críticos (solo ADMIN)."""
    sensores = Sensor.objects.all()

    if request.method == "POST":
        sensor_id = request.POST.get("sensor_id")
        rmin = Decimal(request.POST.get("rango_min"))
        rmax = Decimal(request.POST.get("rango_max"))
        actualizar_umbrales(sensor_id, rmin, rmax, request.user)
        messages.success(request, "Umbrales actualizados correctamente.")
        return redirect("configurar_umbrales")

    return render(request, "sensores/configurar_umbrales.html", {
        "sensores": sensores,
    })


@user_passes_test(es_admin)
def activar_desactivar_sensor(request):
    """Activa o desactiva sensores manualmente."""
    sensores = Sensor.objects.all()
    if request.method == "POST":
        sensor_id = request.POST.get("sensor_id")
        activo = request.POST.get("activo") == "1"
        activar_sensor(sensor_id, activo, request.user)
        messages.success(request, "Sensor actualizado correctamente.")
        return redirect("activar_desactivar_sensor")

    return render(request, "sensores/activar_desactivar.html", {
        "sensores": sensores,
    })
