# core/utils/rut.py

def _solo_digitos(valor: str) -> str:
    return "".join(ch for ch in valor if ch.isdigit())


def calcular_dv(rut_numero: str | int) -> str:
    """
    Calcula el dígito verificador de un RUT chileno
    a partir de los 7 u 8 dígitos sin DV.
    """
    rut_str = str(rut_numero)
    rut_str = _solo_digitos(rut_str)

    if not rut_str.isdigit():
        raise ValueError("El RUT debe contener solo dígitos.")

    num = int(rut_str)
    suma = 0
    multiplicador = 2

    while num > 0:
        suma += (num % 10) * multiplicador
        num //= 10
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    dv = 11 - resto

    if dv == 11:
        return "0"
    if dv == 10:
        return "K"
    return str(dv)


def normalizar_rut_numero(rut_numero: str) -> str:
    """
    Deja el número de RUT solo con dígitos (sin puntos ni guion).
    No hace padding a 8 dígitos, eso se valida aparte.
    """
    rut_str = _solo_digitos(str(rut_numero))
    return rut_str


def validar_rut_completo(rut_numero: str, dv: str) -> bool:
    """
    Valida que el DV entregado corresponda al rut_numero.
    """
    try:
        dv_calculado = calcular_dv(rut_numero)
    except ValueError:
        return False

    return dv_calculado.upper() == str(dv).upper()
