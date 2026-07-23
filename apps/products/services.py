"""Camada de serviços do módulo de Produtos (Arquitetura 06).

Toda regra de negócio relacionada a catálogo, estoque e disponibilidade
vive aqui — nunca nas views ou templates.
"""
from django.db.models import Q, Sum

from .models import Category, Product, ProductImage, ProductVariation

MAX_IMAGES_PER_PRODUCT = 3


class CatalogService:
    """Consultas do catálogo público, respeitando as regras de disponibilidade."""

    @staticmethod
    def available_products():
        """Produtos ativos e com pelo menos uma variação em estoque.

        Produtos inativos ou totalmente esgotados são automaticamente
        removidos do catálogo público (Arquitetura 04).
        """
        return (
            Product.objects.filter(status=Product.STATUS_ACTIVE)
            .annotate(_stock=Sum("variations__stock_quantity"))
            .filter(_stock__gt=0)
            .select_related("category")
            .prefetch_related("images", "variations")
        )

    @staticmethod
    def active_categories():
        """Categorias ativadas pelo admin que possuem produtos disponíveis.

        Só aparecem na loja categorias ativas (Arquitetura 05) com pelo menos
        um produto ativo e em estoque.
        """
        return (
            Category.objects.filter(is_active=True, products__status=Product.STATUS_ACTIVE)
            .annotate(stock=Sum("products__variations__stock_quantity"))
            .filter(stock__gt=0)
            .distinct()
            .order_by("name")
        )

    @classmethod
    def filter_catalog(cls, *, category_slug=None, color=None, size=None,
                       min_price=None, max_price=None, query=None, ordering=None):
        """Aplica filtros e ordenação ao catálogo (Arquitetura 02 - Catálogo/Pesquisa)."""
        qs = cls.available_products()

        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
                | Q(variations__color__icontains=query)
                | Q(variations__size__icontains=query)
            ).distinct()
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if color:
            qs = qs.filter(variations__color__iexact=color).distinct()
        if size:
            qs = qs.filter(variations__size__iexact=size).distinct()
        if min_price not in (None, ""):
            qs = qs.filter(price__gte=min_price)
        if max_price not in (None, ""):
            qs = qs.filter(price__lte=max_price)

        ordering_map = {
            "menor-preco": "price",
            "maior-preco": "-price",
            "nome": "name",
            "recentes": "-created_at",
        }
        qs = qs.order_by(ordering_map.get(ordering, "-created_at"))
        return qs

    @staticmethod
    def get_available_product(slug):
        """Retorna um produto disponível pelo slug, ou None."""
        product = (
            Product.objects.filter(slug=slug)
            .select_related("category")
            .prefetch_related("images", "variations")
            .first()
        )
        if product and product.is_available:
            return product
        return None


class StockService:
    """Regras de estoque, controladas por variação (Arquitetura 04)."""

    @staticmethod
    def get_variation(variation_id):
        return ProductVariation.objects.select_related("product").filter(id=variation_id).first()

    @staticmethod
    def has_stock(variation, quantity):
        return variation is not None and quantity > 0 and variation.stock_quantity >= quantity

    @staticmethod
    def decrease(variation, quantity):
        """Baixa de estoque sem permitir valor negativo."""
        if quantity <= 0:
            return
        new_value = max(0, variation.stock_quantity - quantity)
        variation.stock_quantity = new_value
        variation.save(update_fields=["stock_quantity", "updated_at"])

    @staticmethod
    def set_quantity(variation, quantity):
        variation.stock_quantity = max(0, int(quantity))
        variation.save(update_fields=["stock_quantity", "updated_at"])


class ProductImageService:
    """Gerencia o upload de imagens respeitando o limite de 3 por produto."""

    @staticmethod
    def can_add_image(product):
        return product.images.count() < MAX_IMAGES_PER_PRODUCT

    @classmethod
    def add_image(cls, product, image_file):
        if not cls.can_add_image(product):
            raise ValueError(f"Cada produto pode ter no máximo {MAX_IMAGES_PER_PRODUCT} imagens.")
        order = product.images.count()
        return ProductImage.objects.create(product=product, image=image_file, order=order)
