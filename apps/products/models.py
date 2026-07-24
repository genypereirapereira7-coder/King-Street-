from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Category(TimeStampedModel):
    """Categoria de produtos (Arquitetura 03 - item 5)."""

    name = models.CharField("nome", max_length=120, unique=True)
    slug = models.SlugField("slug", max_length=140, unique=True, blank=True)
    description = models.TextField("descrição", blank=True)
    is_active = models.BooleanField("ativa", default=True)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140]
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    """Produto do catálogo (Arquitetura 03 - item 4)."""

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Ativo"),
        (STATUS_INACTIVE, "Inativo"),
    ]

    name = models.CharField("nome", max_length=160)
    slug = models.SlugField("slug", max_length=180, unique=True, blank=True)
    description = models.TextField("descrição")
    price = models.DecimalField(
        "preço", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # Produto não pode existir sem categoria
        related_name="products",
        verbose_name="categoria",
    )
    status = models.CharField(
        "status", max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE
    )

    class Meta:
        verbose_name = "produto"
        verbose_name_plural = "produtos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:170] or "produto"
            slug = base
            n = 2
            while Product.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base}-{n}"[:180]
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # ---- Consultas de apoio (sem regra de negócio pesada) ----
    @property
    def has_image(self):
        return bool(self.main_image)

    @property
    def is_available(self):
        """Disponível no catálogo público: ativo e com pelo menos uma foto.

        A loja não controla quantidade em estoque — quando um produto acaba,
        o administrador simplesmente o desativa no painel. Produto sem foto
        também não aparece para o cliente.
        """
        return self.status == self.STATUS_ACTIVE and self.has_image

    @property
    def main_image(self):
        # Usa o prefetch quando disponível (ProductImage já vem ordenado pelo
        # Meta.ordering). Um .order_by() aqui dispararia uma consulta por
        # produto na listagem — o painel e o catálogo ficariam lentos.
        imagens = list(self.images.all())
        return imagens[0] if imagens else None

    @property
    def colors(self):
        return sorted({v.color for v in self.variations.all() if v.color})

    @property
    def sizes(self):
        return sorted({v.size for v in self.variations.all() if v.size})


class ProductImage(TimeStampedModel):
    """Imagem do produto — até 3 por produto (Arquitetura 03 - item 6)."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="produto"
    )
    image = models.ImageField("imagem", upload_to="products/%Y/%m/")
    order = models.PositiveSmallIntegerField("ordem", default=0)

    class Meta:
        verbose_name = "imagem do produto"
        verbose_name_plural = "imagens dos produtos"
        ordering = ["order", "id"]

    def __str__(self):
        return f"Imagem {self.order} de {self.product.name}"


class ProductVariation(TimeStampedModel):
    """Variação (cor + tamanho) com estoque próprio (Arquitetura 03 - item 7)."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variations",
        verbose_name="produto",
    )
    color = models.CharField("cor", max_length=40)
    size = models.CharField("tamanho", max_length=40)
    # Campo legado: a loja não controla mais quantidade em estoque.
    # Mantido apenas para preservar os dados já gravados.
    stock_quantity = models.PositiveIntegerField("estoque", default=0)

    class Meta:
        verbose_name = "variação"
        verbose_name_plural = "variações"
        ordering = ["color", "size"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "color", "size"], name="uniq_variation_product_color_size"
            )
        ]
        indexes = [models.Index(fields=["product"])]

    def __str__(self):
        return f"{self.product.name} — {self.color}/{self.size}"

    @property
    def label(self):
        return f"{self.color} · {self.size}"
