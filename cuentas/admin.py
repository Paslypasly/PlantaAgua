# cuentas/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del usuario personalizado para el admin de Django.
    Sin inventar campos raros (como usable_password).
    """

    model = Usuario

    # columnas en el listado
    list_display = (
        "username",
        "email",
        "rol",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "rol",
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )

    # campos al editar un usuario existente
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Información personal",
            {"fields": ("first_name", "last_name", "email", "rut_numero", "rut_dv")},
        ),
        (
            "Rol y permisos",
            {
                "fields": (
                    "rol",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Fechas importantes", {"fields": ("last_login", "date_joined")}),
    )

    # campos al crear un usuario nuevo desde el admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "rol",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ("username", "email", "rut_numero")
    ordering = ("username",)
