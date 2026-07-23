"""Camada de serviços do módulo de Avaliações (Arquitetura 06)."""
from apps.orders.models import Order, OrderStatus

from .models import Review, ReviewImage

MAX_IMAGES_PER_REVIEW = 3


class ReviewService:
    @staticmethod
    def customer_bought_product(customer, product):
        """Verifica se o cliente possui pedido contendo o produto (Arquitetura 04)."""
        if customer is None:
            return False
        return (
            Order.objects.filter(customer=customer, items__product=product)
            .exclude(status=OrderStatus.CANCELED)
            .exists()
        )

    @classmethod
    def can_review(cls, customer, product):
        if not cls.customer_bought_product(customer, product):
            return False
        return not Review.objects.filter(customer=customer, product=product).exists()

    @classmethod
    def create_review(cls, customer, product, rating, comment, images=None):
        if not cls.customer_bought_product(customer, product):
            raise ValueError("Você só pode avaliar produtos que comprou.")
        if Review.objects.filter(customer=customer, product=product).exists():
            raise ValueError("Você já avaliou este produto.")
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError("A nota deve ser entre 1 e 5.")

        review = Review.objects.create(
            customer=customer, product=product, rating=rating, comment=(comment or "").strip()
        )
        for index, image in enumerate((images or [])[:MAX_IMAGES_PER_REVIEW]):
            ReviewImage.objects.create(review=review, image=image, order=index)
        return review

    @staticmethod
    def visible_for_product(product):
        return (
            Review.objects.filter(product=product, is_hidden=False)
            .select_related("customer")
            .prefetch_related("images")
        )
