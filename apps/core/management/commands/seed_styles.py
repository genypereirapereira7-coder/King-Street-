"""Cadastra o catálogo de estilos masculinos (categorias) para o admin ativar.

Cria as categorias que ainda não existem como INATIVAS — o administrador
decide quais aparecem na loja ativando-as no painel. Categorias já
existentes (e seus estados) são preservadas.

Roda automaticamente a cada deploy (ver Procfile) e também na migração
`products.0003_seed_styles`, para que um banco novo já nasça com todos
os estilos disponíveis.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.products.models import Category
from apps.products.style_catalog import iter_styles


class Command(BaseCommand):
    help = "Cadastra os estilos masculinos como categorias (inativas por padrão)."

    def handle(self, *args, **options):
        created = 0
        # Slugs já usados (nomes diferentes podem gerar o mesmo slug, que é único)
        usados = set(Category.objects.values_list("slug", flat=True))
        for nome, grupo in iter_styles():
            if Category.objects.filter(name=nome).exists():
                continue
            slug = slugify(nome)[:140]
            if slug in usados:
                # Já existe uma categoria equivalente (ex.: só muda maiúscula/acento)
                continue
            Category.objects.create(
                name=nome, slug=slug, description=grupo, is_active=False
            )
            usados.add(slug)
            created += 1
        total = Category.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"{created} novo(s) estilo(s) cadastrado(s). Total de categorias: {total}."
        ))
