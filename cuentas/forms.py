# cuentas/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from core.utils import rut as rut_utils


class UsuarioCreationForm(UserCreationForm):
    rut_numero = forms.CharField(
        max_length=8,
        label="RUT (sin DV)",
        help_text="Ingrese solo los números, sin puntos ni guion."
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rut_numero", "rol")

    def clean_rut_numero(self):
        rut_num = rut_utils.normalizar_rut_numero(self.cleaned_data["rut_numero"])
        if len(rut_num) not in (7, 8):
            raise forms.ValidationError("El RUT debe tener 7 u 8 dígitos.")
        return rut_num


class UsuarioChangeForm(UserChangeForm):
    rut_numero = forms.CharField(
        max_length=8,
        label="RUT (sin DV)",
        required=False
    )

    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rut_numero", "rol")

    def clean_rut_numero(self):
        rut_num = self.cleaned_data.get("rut_numero")
        if not rut_num:
            return rut_num
        rut_num = rut_utils.normalizar_rut_numero(rut_num)
        if len(rut_num) not in (7, 8):
            raise forms.ValidationError("El RUT debe tener 7 u 8 dígitos.")
        return rut_num
