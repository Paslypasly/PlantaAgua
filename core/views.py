from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "pages/home.html"


def error_403_view(request, exception):
    """
    Vista para manejar errores 403 (permiso denegado).
    """
    return render(request, "403.html", status=403)


def error_404_view(request, exception):
    """
    Vista para manejar errores 404 (página no encontrada).
    """
    return render(request, "404.html", status=404)


def error_500_view(request):
    """
    Vista para manejar errores 500 (error interno).
    """
    return render(request, "500.html", status=500)
