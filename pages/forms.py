# pages/forms.py
from django import forms


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=120,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ej: Juan Pérez",
        }),
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Ej: nombre@correo.cl",
        }),
    )
    telefono = forms.CharField(
        label="Teléfono (opcional)",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "+56 9 1234 5678",
            "inputmode": "tel",
        }),
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Cuéntanos en qué podemos ayudarte...",
        }),
    )
