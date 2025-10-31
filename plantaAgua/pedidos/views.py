from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from .models import Pedido

def dashboard_pedidos(request):
    estado_filtro = request.GET.get("estado") or ""
    qs = Pedido.objects.select_related("cliente","planta").order_by("-fecha")
    if estado_filtro:
        qs = qs.filter(estado=estado_filtro)

    # Stats por estado
    stats = list(Pedido.objects.values("estado").annotate(total=Count("id")).order_by())

    # KPIs
    hoy = timezone.now().date()
    kpis = {
        "entregado": Pedido.objects.filter(estado="ENTREGADO").count(),
        "en_ruta": Pedido.objects.filter(estado="EN_RUTA").count(),
        "preparacion": Pedido.objects.filter(estado="PREPARACION").count(),
        "ventas_hoy": (Pedido.objects.filter(fecha__date=hoy).aggregate(s=Sum("total"))["s"] or 0),
    }

    # Serie últimos 7 días
    desde = timezone.now() - timezone.timedelta(days=6)
    serie = (Pedido.objects
                .filter(fecha__date__gte=desde.date())
                .annotate(d=TruncDate("fecha"))
                .values("d").annotate(c=Count("id")).order_by("d"))
    labels = [r["d"].strftime("%d-%m") for r in serie]
    cantidades = [r["c"] for r in serie]

    # Dona por estado
    mapa = {"RECIBIDO":0, "PREPARACION":0, "EN_RUTA":0, "ENTREGADO":0, "FALLIDO":0}
    for r in Pedido.objects.values("estado").annotate(c=Count("id")):
        mapa[r["estado"]] = r["c"]
    chart_estados = {
        "labels": list(mapa.keys()),
        "valores": list(mapa.values())
    }

    return render(request, "pedidos/dashboard.html", {
        "pedidos": qs[:200],
        "stats": stats,
        "estado_filtro": estado_filtro,
        "kpis": kpis,
        "chart": {"labels": labels, "cantidades": cantidades},
        "chart_estados": chart_estados,
    })
