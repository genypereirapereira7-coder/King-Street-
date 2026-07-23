from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel


class Coupon(TimeStampedModel):
    """Cupom de desconto (Arquitetura 03 - item 13)."""

    TYPE_FIXED = "fixed"
    TYPE_PERCENT = "percent"
    TYPE_CHOICES = [
        (TYPE_FIXED, "Valor fixo"),
        (TYPE_PERCENT, "Percentual"),
    ]

    code = models.CharField("código", max_length=40, unique=True)
    type = models.CharField("tipo", max_length=10, choices=TYPE_CHOICES, default=TYPE_PERCENT)
    value = models.DecimalField(
        "valor", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    start_date = models.DateField("início")
    end_date = models.DateField("vencimento")
    is_active = models.BooleanField("ativo", default=True)
    max_uses = models.PositiveIntegerField("usos máximos", null=True, blank=True)
    used_count = models.PositiveIntegerField("usos", default=0)

    class Meta:
        verbose_name = "cupom"
        verbose_name_plural = "cupons"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["code"])]

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    @property
    def uses_left(self):
        if self.max_uses is None:
            return None
        return max(0, self.max_uses - self.used_count)
