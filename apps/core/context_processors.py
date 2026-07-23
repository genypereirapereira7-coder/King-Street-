from django.conf import settings

from apps.cart.services import CartService


def store_context(request):
    """Disponibiliza informações globais da loja para todos os templates."""
    try:
        # count() revalida o carrinho: remove itens de produtos desativados
        # ou esgotados, mantendo o contador do topo sempre correto.
        cart_count = CartService(request).count()
    except Exception:
        cart_count = 0

    return {
        "STORE_NAME": settings.STORE_NAME,
        "STORE_WHATSAPP": settings.STORE_WHATSAPP,
        "cart_count": cart_count,
    }
