from django.db import models

from apps.core.models import TimeStampedModel


class Customer(TimeStampedModel):
    """Cliente da loja (Arquitetura 03 - item 8).

    Não há cadastro tradicional: os dados são preenchidos apenas na
    finalização do pedido e reutilizados no mesmo dispositivo via sessão.
    O telefone é usado como identificador natural do comprador.
    """

    name = models.CharField("nome", max_length=160)
    phone = models.CharField("telefone", max_length=20, unique=True)
    address = models.CharField("endereço", max_length=200, blank=True)
    complement = models.CharField("complemento", max_length=120, blank=True)
    neighborhood = models.CharField("bairro", max_length=120, blank=True)
    city = models.CharField("cidade", max_length=120, blank=True)
    zip_code = models.CharField("CEP", max_length=15, blank=True)
    first_order_date = models.DateTimeField("primeiro pedido", null=True, blank=True)
    last_order_date = models.DateTimeField("última compra", null=True, blank=True)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ["name"]
        indexes = [models.Index(fields=["phone"]), models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.name} ({self.phone})"

    @property
    def full_address(self):
        parts = [self.address, self.complement, self.neighborhood, self.city, self.zip_code]
        return ", ".join(p for p in parts if p)

    @property
    def total_orders(self):
        return self.orders.count()
