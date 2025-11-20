# clientes/forms.py
from django import forms
from .models import Cliente
from core.utils import rut as rut_utils


class ClienteForm(forms.ModelForm):
    rut_numero = forms.CharField(
        max_length=8,
        label="RUT (sin DV)",
        help_text="Ingrese solo los números, sin puntos ni guion."
    )

    class Meta:
        model = Cliente
        fields = [
            "rut_numero",
            "nombre",
            "direccion",
            "email",
            "telefono",
            "sector_entrega",
            "activo",
        ]

    def clean_rut_numero(self):
        rut_num = rut_utils.normalizar_rut_numero(self.cleaned_data["rut_numero"])
        if len(rut_num) not in (7, 8):
            raise forms.ValidationError("El RUT debe tener 7 u 8 dígitos.")
        return rut_num
