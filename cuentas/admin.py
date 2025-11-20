# cuentas/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario

    list_display = ("username", "email", "rol", "rut_completo", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Datos adicionales", {"fields": ("rol", "rut_numero", "rut_dv")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Datos adicionales", {"fields": ("rol", "rut_numero")}),
    )
