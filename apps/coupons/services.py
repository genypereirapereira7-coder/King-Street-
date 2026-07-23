"""Camada de serviços do módulo de Cupons (Arquitetura 06)."""
from decimal import Decimal

from django.utils import timezone

from .models import Coupon


class CouponService:
    @staticmethod
    def validate(code):
        """Valida um cupom pelo código e devolve o objeto, ou levanta ValueError."""
        code = (code or "").strip().upper()
        if not code:
            raise ValueError("Informe um cupom.")
        coupon = Coupon.objects.filter(code=code).first()
        if not coupon:
            raise ValueError("Cupom inválido.")
        if not coupon.is_active:
            raise ValueError("Cupom inativo.")
        today = timezone.localdate()
        if today < coupon.start_date:
            raise ValueError("Cupom ainda não está válido.")
        if today > coupon.end_date:
            raise ValueError("Cupom expirado.")
        if coupon.max_uses is not None and coupon.used_count >= coupon.max_uses:
            raise ValueError("Cupom esgotado.")
        return coupon

    @staticmethod
    def calculate_discount(coupon, subtotal):
        subtotal = Decimal(subtotal)
        if coupon.type == Coupon.TYPE_PERCENT:
            discount = subtotal * (coupon.value / Decimal("100"))
        else:
            discount = coupon.value
        discount = min(discount, subtotal)
        return discount.quantize(Decimal("0.01"))

    @staticmethod
    def register_use(coupon):
        coupon.used_count = coupon.used_count + 1
        coupon.save(update_fields=["used_count", "updated_at"])
