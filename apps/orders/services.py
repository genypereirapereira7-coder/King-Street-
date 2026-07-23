"""Camada de serviços do módulo de Pedidos (Arquitetura 06).

Concentra a criação do pedido a partir do carrinho, a baixa de estoque,
o controle de status com histórico e a montagem da mensagem do WhatsApp.
"""
import logging
from decimal import Decimal
from urllib.parse import quote

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.coupons.services import CouponService
from apps.customers.services import CustomerService
from apps.products.services import StockService

from .models import DeliveryMethod, Order, OrderItem, OrderStatus, OrderStatusHistory

logger = logging.getLogger("kingstreet")


class OrderService:
    @staticmethod
    def _generate_number():
        prefix = timezone.now().strftime("%Y%m%d")
        last = (
            Order.objects.filter(number__startswith=prefix)
            .order_by("-number")
            .values_list("number", flat=True)
            .first()
        )
        seq = int(last.split("-")[1]) + 1 if last else 1
        return f"{prefix}-{seq:04d}"

    @classmethod
    @transaction.atomic
    def create_from_cart(cls, request, cart, customer_data):
        """Cria o pedido antes do redirecionamento ao WhatsApp (Arquitetura 04).

        Valida estoque no servidor, dá baixa por variação, registra o cliente,
        aplica o cupom e cria o histórico inicial.
        """
        items = cart.items()
        if not items:
            raise ValueError("Carrinho vazio.")

        delivery_method = customer_data.get("delivery_method")
        if delivery_method not in dict(DeliveryMethod.choices):
            raise ValueError("Forma de entrega inválida.")

        # Revalida o estoque de cada item no servidor
        for item in items:
            variation = StockService.get_variation(item.variation_id)
            if not StockService.has_stock(variation, item.quantity):
                raise ValueError(
                    f"Estoque insuficiente para {item.product.name} "
                    f"({item.variation.label})."
                )

        customer = CustomerService.get_or_create_customer(customer_data)

        subtotal = cart.subtotal()
        coupon = cart.coupon()
        discount = cart.discount()
        total = max(Decimal("0.00"), subtotal - discount)

        delivery_address = ""
        if delivery_method == DeliveryMethod.DELIVERY:
            delivery_address = customer.full_address

        order = Order.objects.create(
            number=cls._generate_number(),
            customer=customer,
            delivery_method=delivery_method,
            status=OrderStatus.RECEIVED,
            delivery_address=delivery_address,
            subtotal=subtotal,
            discount=discount,
            total=total,
            coupon_code=coupon.code if coupon else "",
            notes=customer_data.get("notes", "").strip(),
        )

        for item in items:
            variation = item.variation
            OrderItem.objects.create(
                order=order,
                product=variation.product,
                variation=variation,
                product_name=variation.product.name,
                variation_label=variation.label,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            # Baixa de estoque por variação
            StockService.decrease(variation, item.quantity)

        OrderStatusHistory.objects.create(
            order=order, previous_status="", new_status=OrderStatus.RECEIVED,
            note="Pedido criado.",
        )

        if coupon:
            CouponService.register_use(coupon)

        CustomerService.register_order_dates(customer)
        logger.info("Pedido criado: %s", order.number)
        return order

    @staticmethod
    @transaction.atomic
    def change_status(order, new_status, note=""):
        """Altera o status registrando o histórico (Arquitetura 04)."""
        if new_status not in dict(OrderStatus.choices):
            raise ValueError("Status inválido.")
        if new_status == order.status:
            return order
        previous = order.status
        order.status = new_status
        order.save(update_fields=["status", "updated_at"])
        OrderStatusHistory.objects.create(
            order=order, previous_status=previous, new_status=new_status, note=note
        )
        logger.info("Pedido %s -> %s", order.number, new_status)
        return order


class WhatsAppService:
    """Monta a mensagem estruturada e a URL do WhatsApp (Arquitetura 02)."""

    @staticmethod
    def _brl(value):
        inteiro, _, cent = f"{Decimal(value):.2f}".partition(".")
        partes = []
        while len(inteiro) > 3:
            partes.insert(0, inteiro[-3:])
            inteiro = inteiro[:-3]
        partes.insert(0, inteiro)
        return f"R$ {'.'.join(partes)},{cent}"

    @classmethod
    def build_message(cls, order):
        c = order.customer
        lines = [
            f"*{settings.STORE_NAME} — Novo Pedido*",
            f"Pedido: *{order.number}*",
            "",
            "*Cliente*",
            f"Nome: {c.name}",
            f"Telefone: {c.phone}",
        ]

        if order.is_delivery:
            lines += ["", "*Entrega*", f"Endereço: {order.delivery_address or c.full_address}"]
        else:
            lines += ["", "*Retirada na loja*"]

        lines += ["", "*Itens*"]
        for item in order.items.all():
            variation = f" ({item.variation_label})" if item.variation_label else ""
            lines.append(
                f"• {item.quantity}x {item.product_name}{variation} — "
                f"{cls._brl(item.total_price)}"
            )

        lines += ["", f"Subtotal: {cls._brl(order.subtotal)}"]
        if order.discount and order.discount > 0:
            cupom = f" ({order.coupon_code})" if order.coupon_code else ""
            lines.append(f"Desconto{cupom}: -{cls._brl(order.discount)}")
        lines.append(f"*Total: {cls._brl(order.total)}*")

        if order.notes:
            lines += ["", f"Observações: {order.notes}"]

        return "\n".join(lines)

    @classmethod
    def build_url(cls, order, phone=None):
        phone = phone or settings.STORE_WHATSAPP
        message = cls.build_message(order)
        return f"https://wa.me/{phone}?text={quote(message)}"
