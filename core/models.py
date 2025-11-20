# core/models.py
from django.db import models


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
    Entidad abstracta con campos de RUT (solo 8 dígitos + DV).
    La validación y cálculo de DV se implementará en FASE 2.
    """
    rut_numero = models.CharField(max_length=8, verbose_name="RUT (sin DV)")
    rut_dv = models.CharField(max_length=1, verbose_name="DV")

    class Meta:
        abstract = True

    @property
    def rut_completo(self) -> str:
        return f"{self.rut_numero}-{self.rut_dv}"

    def __str__(self) -> str:
        return self.rut_completo
