from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def calidad_dashboard(request):
    return render(request, "calidad/dashboard.html", {})
