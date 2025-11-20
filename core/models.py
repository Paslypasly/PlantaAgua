from django.db import models
from .utils import rut as rut_utils

class BaseModel(models.Model):
    """
    Modelo base con campos comunes a casi todas las tablas.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True



class EntidadConRut(BaseModel):
    """
    Entidad abstracta que trabaja con RUT separado:
    - rut_numero: solo dígitos (sin puntos ni guion)
    - rut_dv: '0'-'9' o 'K'
    El DV se calcula automáticamente a partir de rut_numero.
    """
    rut_numero = models.CharField(max_length=8, verbose_name="RUT (sin DV)")
    rut_dv = models.CharField(max_length=1, verbose_name="DV")

    class Meta:
        abstract = True

    def get_rut_completo(self) -> str:
        return f"{self.rut_numero}-{self.rut_dv}"

    @property
    def rut_completo(self) -> str:
        return self.get_rut_completo()

    def clean(self):
        super().clean()
        # Normalizar y validar longitud
        rut_num = rut_utils.normalizar_rut_numero(self.rut_numero)
        if len(rut_num) not in (7, 8):
            raise ValueError("El RUT debe tener 7 u 8 dígitos (sin DV).")
        self.rut_numero = rut_num
        # Calcular DV automáticamente
        self.rut_dv = rut_utils.calcular_dv(self.rut_numero)

    def save(self, *args, **kwargs):
        # Asegurar cálculo de DV incluso si no se llamó clean() desde un form
        rut_num = rut_utils.normalizar_rut_numero(self.rut_numero)
        self.rut_numero = rut_num
        self.rut_dv = rut_utils.calcular_dv(self.rut_numero)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.rut_completo
