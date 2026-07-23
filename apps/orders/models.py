from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel


class OrderStatus(models.TextChoices):
    """Status previstos para o pedido (Arquitetura 03/04)."""

    RECEIVED = "received", "Pedido recebido"
    PREPARING = "preparing", "Em preparação"
    OUT_FOR_DELIVERY = "out_for_delivery", "Saiu para entrega"
    DELIVERED = "delivered", "Entregue"
    CANCELED = "canceled", "Cancelado"


class DeliveryMethod(models.TextChoices):
    PICKUP = "pickup", "Retirada na loja"
    DELIVERY = "delivery", "Entrega local"


class Order(TimeStampedModel):
    """Pedido (Arquitetura 03 - item 10).

    Criado antes do redirecionamento ao WhatsApp, permitindo o
    acompanhamento no painel.
    """

    number = models.CharField("número", max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="cliente",
    )
    delivery_method = models.CharField(
        "forma de entrega", max_length=20, choices=DeliveryMethod.choices
    )
    status = models.CharField(
        "status", max_length=20, choices=OrderStatus.choices, default=OrderStatus.RECEIVED
    )

    # Snapshot do endereço no momento do pedido (quando for entrega)
    delivery_address = models.CharField("endereço de entrega", max_length=300, blank=True)

    subtotal = models.DecimalField("subtotal", max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField("desconto", max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(
        "total", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0
    )
    coupon_code = models.CharField("cupom", max_length=40, blank=True)
    notes = models.TextField("observações", blank=True)

    class Meta:
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["number"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Pedido {self.number}"

    @property
    def is_delivery(self):
        return self.delivery_method == DeliveryMethod.DELIVERY


class OrderItem(TimeStampedModel):
    """Item do pedido (Arquitetura 03 - item 11).

    Guarda o preço praticado no momento da compra para preservar o histórico.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="pedido"
    )
    # SET_NULL preserva o histórico mesmo que o produto seja excluído
    product = models.ForeignKey(
        "products.Product", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="order_items", verbose_name="produto",
    )
    variation = models.ForeignKey(
        "products.ProductVariation", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="order_items", verbose_name="variação",
    )
    # Snapshots (preservam o histórico independente de alterações futuras)
    product_name = models.CharField("produto", max_length=160)
    variation_label = models.CharField("variação", max_length=90, blank=True)
    quantity = models.PositiveIntegerField("quantidade")
    unit_price = models.DecimalField("preço unitário", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "item do pedido"
        verbose_name_plural = "itens do pedido"
        ordering = ["id"]

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    @property
    def total_price(self):
        return self.unit_price * self.quantity


class OrderStatusHistory(TimeStampedModel):
    """Histórico de status do pedido — nunca removido (Arquitetura 03 - item 12)."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="history", verbose_name="pedido"
    )
    previous_status = models.CharField(
        "status anterior", max_length=20, choices=OrderStatus.choices, blank=True
    )
    new_status = models.CharField("novo status", max_length=20, choices=OrderStatus.choices)
    note = models.CharField("observação", max_length=200, blank=True)

    class Meta:
        verbose_name = "histórico do pedido"
        verbose_name_plural = "históricos dos pedidos"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.order.number}: {self.get_new_status_display()}"
