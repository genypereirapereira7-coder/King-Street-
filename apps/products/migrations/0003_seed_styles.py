"""Popula as categorias com o catálogo de estilos masculinos.

Idempotente: só cria os estilos que ainda não existem e nunca altera os
já cadastrados (nem o estado ativo/inativo escolhido pelo admin).
"""
from django.db import migrations
from django.utils.text import slugify

from apps.products.style_catalog import iter_styles


def seed_styles(apps, schema_editor):
    Category = apps.get_model("products", "Category")
    nomes = set(Category.objects.values_list("name", flat=True))
    slugs = set(Category.objects.values_list("slug", flat=True))
    novos = []
    for nome, grupo in iter_styles():
        slug = slugify(nome)[:140]
        # Pula nomes já existentes e slugs já usados (o slug é único e nomes
        # diferentes podem gerar o mesmo, ex.: maiúscula/acento).
        if nome in nomes or slug in slugs:
            continue
        novos.append(Category(name=nome, slug=slug, description=grupo, is_active=False))
        nomes.add(nome)
        slugs.add(slug)
    Category.objects.bulk_create(novos, ignore_conflicts=True)


def noop(apps, schema_editor):
    """Não remove nada no rollback: os estilos podem já ter produtos."""


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_remove_product_products_pr_sku_ca0cdc_idx_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_styles, noop),
    ]
