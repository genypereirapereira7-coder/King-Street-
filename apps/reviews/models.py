from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel


class Review(TimeStampedModel):
    """Avaliação de produto (Arquitetura 03 - item 14).

    Somente clientes que compraram o produto podem avaliar.
    """

    customer = models.ForeignKey(
        "customers.Customer", on_delete=models.CASCADE,
        related_name="reviews", verbose_name="cliente",
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE,
        related_name="reviews", verbose_name="produto",
    )
    rating = models.PositiveSmallIntegerField(
        "nota", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField("comentário", blank=True)
    is_hidden = models.BooleanField("oculta", default=False)

    class Meta:
        verbose_name = "avaliação"
        verbose_name_plural = "avaliações"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "product"], name="uniq_review_customer_product"
            )
        ]

    def __str__(self):
        return f"{self.product} — {self.rating}★"


class ReviewImage(TimeStampedModel):
    """Imagem da avaliação — até 3 por avaliação (Arquitetura 03 - item 15)."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="images", verbose_name="avaliação"
    )
    image = models.ImageField("imagem", upload_to="reviews/%Y/%m/")
    order = models.PositiveSmallIntegerField("ordem", default=0)

    class Meta:
        verbose_name = "imagem da avaliação"
        verbose_name_plural = "imagens das avaliações"
        ordering = ["order", "id"]

    def __str__(self):
        return f"Imagem {self.order} da avaliação {self.review_id}"
