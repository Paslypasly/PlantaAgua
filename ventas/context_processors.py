from .services import CartService


def cart_context(request):
    """
    Agrega datos del carrito al contexto global de templates:

    - cart_item_count: cantidad total de ítems en el carrito
    - cart_total: total del carrito
    """
    try:
        cart = CartService(request)
        item_count = 0
        for item in cart:
            item_count += item["cantidad"]
        total = cart.total()
    except Exception:
        item_count = 0
        total = 0

    return {
        "cart_item_count": item_count,
        "cart_total": total,
    }
