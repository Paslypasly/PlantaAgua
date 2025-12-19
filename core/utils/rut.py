# core/utils/rut.py

def normalizar_rut_numero(valor: str) -> str:
    """
    Limpia el RUT y deja solo dígitos (sin puntos, sin guion, sin DV).
    Ej: "12.345.678" -> "12345678"
    """
    if valor is None:
        return ""
    s = str(valor).strip().replace(".", "").replace("-", "").replace(" ", "")
    # si alguien mete el DV pegado (ej: 12345678K), lo cortamos
    # porque este helper es "sin DV"
    if len(s) >= 2 and (s[-1].upper() == "K" or s[-1].isdigit()):
        # si el string tiene letras o es largo, intentamos dejar solo dígitos
        # (en tu form pides sin DV, así que esto es para “defenderse”)
        pass
    return "".join(ch for ch in s if ch.isdigit())


def calcular_dv(rut_numero: str) -> str:
    """
    Calcula DV del RUT (módulo 11).
    Recibe SOLO el número (sin DV).
    Retorna '0'..'9' o 'K'.
    """
    rut = normalizar_rut_numero(rut_numero)
    if not rut or not rut.isdigit():
        return ""

    reversed_digits = list(map(int, reversed(rut)))
    factors = [2, 3, 4, 5, 6, 7]
    s = 0
    for i, d in enumerate(reversed_digits):
        s += d * factors[i % len(factors)]

    mod = 11 - (s % 11)
    if mod == 11:
        return "0"
    if mod == 10:
        return "K"
    return str(mod)


def validar_rut_completo(rut_numero: str, dv: str) -> bool:
    """
    Valida (rut, dv). DV puede venir en minúscula.
    """
    if rut_numero is None or dv is None:
        return False

    rut = normalizar_rut_numero(rut_numero)
    dv_in = str(dv).strip().upper()

    if not rut or not rut.isdigit():
        return False
    if dv_in not in "0123456789K":
        return False

    return calcular_dv(rut) == dv_in
