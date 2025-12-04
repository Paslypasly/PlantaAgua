from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from .models import Notificacion
from .services import marcar_notificaciones_como_leidas


class NotificacionListView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = "notificaciones/lista.html"
    context_object_name = "notificaciones"

    def get_queryset(self):
        return Notificacion.objects.filter(
            usuario=self.request.user
        ).order_by("-created_at")
        # asumiendo que BaseModel tiene created_at


class NotificacionMarcarLeidasView(LoginRequiredMixin, View):
    def post(self, request):
        marcar_notificaciones_como_leidas(request.user)
        return redirect(reverse_lazy("notificaciones:lista"))
