"""Camada de serviços do Carrinho (Arquitetura 02/04).

O carrinho é mantido na sessão persistente do cliente. Cada item referencia
uma variação de produto (cor + tamanho). A loja não controla quantidade em
estoque: um item só sai do carrinho se o produto for desativado pelo
administrador ou se a variação for removida. Totais e cupom ficam aqui.
"""
from decimal import Decimal

from apps.coupons.services import CouponService
from apps.products.services import StockService

CART_SESSION_KEY = "cart"
COUPON_SESSION_KEY = "cart_coupon"


class CartItem:
    """Representa uma linha do carrinho já resolvida com dados do produto."""

    def __init__(self, variation, quantity):
        self.variation = variation
        self.product = variation.product
        self.quantity = quantity
        self.unit_price = product_price = variation.product.price
        self.total_price = product_price * quantity

    @property
    def variation_id(self):
        return self.variation.id


class CartService:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = self.session.setdefault(CART_SESSION_KEY, {})

    # ---- Persistência ----
    def _save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def clear(self):
        """Esvazia o carrinho (chamado após o redirecionamento ao WhatsApp)."""
        self.session[CART_SESSION_KEY] = {}
        self.session.pop(COUPON_SESSION_KEY, None)
        self.session.modified = True
        self.cart = self.session[CART_SESSION_KEY]

    # ---- Operações ----
    def add(self, variation_id, quantity=1):
        """Adiciona uma variação ao carrinho."""
        variation = StockService.get_variation(variation_id)
        if variation is None:
            raise ValueError("Variação não encontrada.")
        if not StockService.is_available(variation, 1):
            raise ValueError("Produto indisponível no momento.")

        key = str(variation_id)
        self.cart[key] = self.cart.get(key, 0) + max(1, int(quantity))
        self._save()

    def set_quantity(self, variation_id, quantity):
        variation = StockService.get_variation(variation_id)
        quantity = int(quantity)
        if variation is None or quantity <= 0:
            self.remove(variation_id)
            return
        self.cart[str(variation_id)] = quantity
        self._save()

    def remove(self, variation_id):
        self.cart.pop(str(variation_id), None)
        self._save()

    # ---- Consulta ----
    def items(self):
        items = []
        variation_ids = [int(k) for k in self.cart.keys()]
        variations = {v.id: v for v in _load_variations(variation_ids)}
        changed = False
        for key, quantity in list(self.cart.items()):
            variation = variations.get(int(key))
            # Remove se a variação não existe mais
            if variation is None:
                del self.cart[key]
                changed = True
                continue
            product = variation.product
            # Remove se o produto foi DESATIVADO pelo administrador
            if product.status != product.STATUS_ACTIVE:
                del self.cart[key]
                changed = True
                continue
            items.append(CartItem(variation, quantity))
        if changed:
            self._save()
        return items

    def total_items(self):
        """Soma bruta das quantidades na sessão (sem revalidar)."""
        return sum(self.cart.values())

    def count(self):
        """Quantidade total de itens VÁLIDOS (revalida e limpa o carrinho)."""
        return sum(item.quantity for item in self.items())

    def is_empty(self):
        return not self.cart

    def subtotal(self):
        return sum((item.total_price for item in self.items()), Decimal("0.00"))

    # ---- Cupom ----
    def apply_coupon(self, code):
        coupon = CouponService.validate(code)
        self.session[COUPON_SESSION_KEY] = coupon.code
        self.session.modified = True
        return coupon

    def remove_coupon(self):
        self.session.pop(COUPON_SESSION_KEY, None)
        self.session.modified = True

    def coupon(self):
        code = self.session.get(COUPON_SESSION_KEY)
        if not code:
            return None
        try:
            return CouponService.validate(code)
        except ValueError:
            self.remove_coupon()
            return None

    def discount(self):
        coupon = self.coupon()
        if not coupon:
            return Decimal("0.00")
        return CouponService.calculate_discount(coupon, self.subtotal())

    def total(self):
        return max(Decimal("0.00"), self.subtotal() - self.discount())


def _load_variations(ids):
    from apps.products.models import ProductVariation

    if not ids:
        return []
    return ProductVariation.objects.select_related("product").filter(id__in=ids)
