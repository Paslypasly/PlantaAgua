from django import forms

from clientes.models import SectorEntrega
from core.utils.rut import normalizar_rut_numero


class CheckoutPublicoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=150,
    )
    correo = forms.EmailField(
        label="Correo electrónico",
    )
    telefono = forms.CharField(
        label="Teléfono de contacto",
        max_length=20,
    )
    direccion = forms.CharField(
        label="Dirección de entrega",
        max_length=255,
        widget=forms.Textarea(attrs={"rows": 2}),
    )
    sector_entrega = forms.ModelChoiceField(
        label="Sector de entrega",
        queryset=SectorEntrega.objects.all(),
    )

    rut_numero = forms.CharField(
        label="RUT (sin DV, opcional)",
        max_length=8,
        required=False,
        help_text="Ingrese solo los 7 u 8 dígitos, sin puntos ni guion. El DV se calcula automáticamente.",
    )

    forma_pago = forms.ChoiceField(
        label="Forma de pago",
        choices=(
            ("EFECTIVO", "Efectivo (al momento de la entrega)"),
            ("TRANSFERENCIA", "Transferencia bancaria"),
        ),
        initial="EFECTIVO",
        widget=forms.RadioSelect,
    )

    comentarios = forms.CharField(
        label="Comentarios adicionales (opcional)",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def clean_rut_numero(self):
        rut = self.cleaned_data.get("rut_numero", "").strip()
        if not rut:
            return ""

        rut_normalizado = normalizar_rut_numero(rut)
        if not rut_normalizado.isdigit():
            raise forms.ValidationError("El RUT debe contener solo dígitos.")
        if len(rut_normalizado) not in (7, 8):
            raise forms.ValidationError("El RUT debe tener 7 u 8 dígitos.")
        return rut_normalizado
