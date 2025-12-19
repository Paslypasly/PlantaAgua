from django.db import models
from .utils import rut as rut_utils
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

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
    Guarda RUT separado en:
    - rut: número SIN DV (ej: 21734979)
    - dv: dígito verificador (0-9 o K)
    Ambos opcionales.
    """
    rut = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name="RUT (sin DV)",
        help_text="Sin puntos ni guion, solo los 7 u 8 dígitos."
    )
    dv = models.CharField(
        max_length=1,
        blank=True,
        default="",
        verbose_name="DV"
    )

    class Meta:
        abstract = True

    @staticmethod
    def calcular_dv(rut: str) -> str:
        """
        Algoritmo módulo 11 para DV chileno.
        """
        rut_str = str(rut).strip()
        if not rut_str.isdigit():
            return ""
        serie = [2, 3, 4, 5, 6, 7]
        suma = 0
        j = 0
        for dig in reversed(rut_str):
            suma += int(dig) * serie[j]
            j = (j + 1) % len(serie)

        resto = 11 - (suma % 11)
        if resto == 11:
            return "0"
        if resto == 10:
            return "K"
        return str(resto)

    @property
    def rut_completo(self) -> str:
        if not self.rut:
            return "-"
        dv = (self.dv or self.calcular_dv(self.rut)).upper()
        return f"{self.rut}-{dv}"

    def clean(self):
        super().clean()
        if not self.rut:
            return
        dv_ingresado = (self.dv or "").strip().upper()
        dv_calculado = self.calcular_dv(self.rut)
        if dv_ingresado and dv_ingresado != dv_calculado:
            raise ValidationError({"dv": f"DV inválido. Para {self.rut} debe ser {dv_calculado}."})

    def save(self, *args, **kwargs):
        if self.rut and not (self.dv or "").strip():
            self.dv = self.calcular_dv(self.rut)
        if self.dv:
            self.dv = self.dv.strip().upper()
        self.full_clean()
        return super().save(*args, **kwargs)

