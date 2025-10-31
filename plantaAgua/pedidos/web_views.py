from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from .models import Pedido, PedidoItem, Cliente
from usuarios.models import Planta

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre","rut","telefono","direccion"]

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ["planta","cliente","estado","observacion"]

@login_required
def pedidos_list(request):
    qs = Pedido.objects.select_related("cliente","planta").order_by("-fecha")
    return render(request, "pedidos/list.html", {"pedidos": qs[:200]})

@login_required
def pedido_detail(request, pk):
    ped = get_object_or_404(Pedido.objects.select_related("cliente","planta"), pk=pk)
    items = ped.items.all()
    return render(request, "pedidos/detail.html", {"p": ped, "items": items})

@login_required
def pedido_new(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            ped = form.save()
            return redirect("web_pedido_detail", pk=ped.pk)
    else:
        form = PedidoForm()
    return render(request, "pedidos/form.html", {"form": form, "titulo":"Nuevo Pedido"})

@login_required
def clientes_list(request):
    qs = Cliente.objects.all().order_by("nombre")
    return render(request, "clientes/list.html", {"clientes": qs})

@login_required
def cliente_new(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("web_clientes_list")
    else:
        form = ClienteForm()
    return render(request, "clientes/form.html", {"form": form, "titulo":"Nuevo Cliente"})
