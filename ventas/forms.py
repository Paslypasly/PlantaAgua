# ventas/forms.py
from django import forms
from django.core.validators import RegexValidator

from clientes.models import SectorEntrega
from core.utils.rut import normalizar_rut_numero


class CheckoutPublicoForm(forms.Form):
    """
    Formulario de checkout para cliente público.
    No requiere usuario autenticado.
    """
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=120,
        widget=forms.TextInput(),
    )

    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(),
    )

    telefono = forms.CharField(
        label="Teléfono de contacto",
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?56 ?9 ?\d{4} ?\d{4}$',
                message="Ingrese un número chileno válido, por ejemplo: +56 9 1234 5678.",
            )
        ],
        widget=forms.TextInput(),
    )

    sector_entrega = forms.ModelChoiceField(
        label="Sector de entrega",
        queryset=SectorEntrega.objects.all(),
        empty_label="Seleccione un sector",
    )

    direccion = forms.CharField(
        label="Dirección de entrega",
        widget=forms.Textarea(),
    )

    rut_numero = forms.CharField(
        label="RUT (sin DV, opcional)",
        required=False,
        max_length=8,
        widget=forms.TextInput(),
        help_text="Ingrese solo los 7 u 8 dígitos, sin puntos ni guion. El DV se calcula automáticamente.",
    )

    FORMA_PAGO_CHOICES = [
        ("EFECTIVO", "Efectivo (al momento de la entrega)"),
        ("TRANSFERENCIA", "Transferencia bancaria"),
    ]
    forma_pago = forms.ChoiceField(
        label="Forma de pago",
        choices=FORMA_PAGO_CHOICES,
        widget=forms.RadioSelect(),
        initial="EFECTIVO",
    )

    comentarios = forms.CharField(
        label="Comentarios adicionales (opcional)",
        required=False,
        widget=forms.Textarea(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicar clases de Bootstrap a todos los campos
        for name, field in self.fields.items():
            widget = field.widget

            # Radios
            if isinstance(widget, forms.RadioSelect):
                widget.attrs.setdefault("class", "form-check-input")
            # Selects
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-select")
            # Textareas
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", "form-control")
                widget.attrs.setdefault("rows", 3)
            # Inputs normales
            else:
                widget.attrs.setdefault("class", "form-control")

        # Placeholders específicos
        self.fields["nombre"].widget.attrs.setdefault("placeholder", "Ej: Juan Pérez")
        self.fields["correo"].widget.attrs.setdefault("placeholder", "Ej: nombre@correo.cl")
        self.fields["telefono"].widget.attrs.update(
            {
                "placeholder": "+56 9 1234 5678",
                "inputmode": "tel",
            }
        )
        self.fields["direccion"].widget.attrs.setdefault(
            "placeholder", "Calle, número, depto, ciudad"
        )
        self.fields["comentarios"].widget.attrs.setdefault(
            "placeholder", "Instrucciones especiales de entrega (opcional)"
        )

    def clean_rut_numero(self):
        """
        Rut opcional: si viene, normalizamos y validamos longitud (7 u 8 dígitos).
        El DV se calcula en otra capa.
        """
        data = self.cleaned_data.get("rut_numero", "").strip()
        if not data:
            return ""

        rut_numero = normalizar_rut_numero(data)
        if not rut_numero.isdigit() or len(rut_numero) not in (7, 8):
            raise forms.ValidationError("El RUT debe tener 7 u 8 dígitos numéricos.")

        return rut_numero
