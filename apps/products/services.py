"""Camada de serviços do módulo de Produtos (Arquitetura 06).

Toda regra de negócio relacionada a catálogo, estoque e disponibilidade
vive aqui — nunca nas views ou templates.
"""
from django.db.models import Q

from .models import Category, Product, ProductImage, ProductVariation

MAX_IMAGES_PER_PRODUCT = 3


class CatalogService:
    """Consultas do catálogo público, respeitando as regras de disponibilidade."""

    @staticmethod
    def available_products():
        """Produtos ativos e com pelo menos uma foto.

        A loja não controla quantidade: quando um produto acaba, o
        administrador o desativa e ele sai do catálogo (Arquitetura 04).
        Um produto sem foto nunca aparece para o cliente.
        """
        return (
            Product.objects.filter(status=Product.STATUS_ACTIVE, images__isnull=False)
            .distinct()
            .select_related("category")
            .prefetch_related("images", "variations")
        )

    @staticmethod
    def active_categories():
        """Categorias ativadas pelo admin que possuem produtos ativos."""
        return (
            Category.objects.filter(is_active=True, products__status=Product.STATUS_ACTIVE)
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


class ProductService:
    """Regras de publicação de produtos."""

    @staticmethod
    def has_image(product):
        return product.images.exists()

    @classmethod
    def enforce_photo_before_active(cls, product):
        """Um produto só pode ficar Ativo (visível na loja) com pelo menos
        uma foto. Se estiver ativo sem foto, volta para inativo.

        Retorna True se precisou reverter (para a view avisar o admin).
        """
        if product.status == Product.STATUS_ACTIVE and not cls.has_image(product):
            product.status = Product.STATUS_INACTIVE
            product.save(update_fields=["status", "updated_at"])
            return True
        return False


class StockService:
    """Disponibilidade por variação (Arquitetura 04).

    A loja não trabalha com contagem de estoque: a disponibilidade depende
    apenas do produto estar ativo. Quando uma peça acaba, o administrador
    desativa o produto (ou remove a variação) no painel.
    """

    @staticmethod
    def get_variation(variation_id):
        return ProductVariation.objects.select_related("product").filter(id=variation_id).first()

    @staticmethod
    def is_available(variation, quantity=1):
        """A variação pode ser comprada nesta quantidade?"""
        if variation is None or quantity <= 0:
            return False
        return variation.product.status == Product.STATUS_ACTIVE


class ProductImageService:
    """Gerencia o upload de imagens respeitando o limite de 3 por produto."""

    @staticmethod
    def remaining_slots(product):
        """Quantas fotos ainda cabem neste produto."""
        return max(0, MAX_IMAGES_PER_PRODUCT - product.images.count())

    @classmethod
    def can_add_image(cls, product):
        return cls.remaining_slots(product) > 0

    @classmethod
    def add_image(cls, product, image_file):
        if not cls.can_add_image(product):
            raise ValueError(f"Cada produto pode ter no máximo {MAX_IMAGES_PER_PRODUCT} imagens.")
        order = product.images.count()
        return ProductImage.objects.create(product=product, image=image_file, order=order)

    @classmethod
    def add_images(cls, product, image_files):
        """Envia várias fotos de uma vez, até completar o limite do produto.

        Retorna (quantidade_adicionada, quantidade_ignorada) para que a view
        avise o administrador quando o limite for atingido no meio do envio.
        """
        livres = cls.remaining_slots(product)
        if livres <= 0:
            raise ValueError(f"Cada produto pode ter no máximo {MAX_IMAGES_PER_PRODUCT} fotos.")
        adicionadas = 0
        for image_file in image_files[:livres]:
            cls.add_image(product, image_file)
            adicionadas += 1
        return adicionadas, max(0, len(image_files) - livres)
