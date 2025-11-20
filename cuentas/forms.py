# cuentas/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from core.utils import rut as rut_utils
# cuentas/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
# cuentas/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Usuario
from core.utils import rut as rut_utils


class UsuarioCreationForm(UserCreationForm):
    """
    Formulario para que el ADMIN cree nuevos usuarios del sistema.
    """
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            "username",
            "email",
            "rol",
            "is_active",
            "is_staff",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con ese nombre.")
        return username


class UsuarioChangeForm(UserChangeForm):
    """
    Formulario para editar usuarios existentes.
    """
    password = None  # no mostramos el hash

    class Meta:
        model = Usuario
        fields = (
            "username",
            "email",
            "rol",
            "is_active",
            "is_staff",
        )


class ClienteForm(forms.ModelForm):
    """
    Si estabas usando un form de Cliente aquí, lo dejamos como está.
    (No lo toco si ya lo tienes en clientes/forms.py)
    """
    pass

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "rut_numero",
            "rut_dv",
            "rol",
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # estilos Bootstrap
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != "CheckboxInput":
                field.widget.attrs.setdefault("class", "form-control")

        self.fields["password1"].widget.attrs.setdefault("class", "form-control")
        self.fields["password2"].widget.attrs.setdefault("class", "form-control")


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "email",
            "rut_numero",
            "rut_dv",
            "rol",
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
        # opcional: que el rol no se pueda cambiar desde el perfil
        self.fields["rol"].disabled = True


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
