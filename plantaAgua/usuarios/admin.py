from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Planta


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol', 'planta')}),
    )
    list_display = ('username', 'email', 'rol', 'planta', 'is_staff', 'is_active')
    list_filter = ('rol', 'planta', 'is_staff', 'is_active')


admin.site.register(Rol)
admin.site.register(Planta)
