"""Cadastra o catálogo de estilos masculinos (categorias) para o admin ativar.

Cria as categorias que ainda não existem como INATIVAS — o administrador
decide quais aparecem na loja ativando-as no painel. Categorias já
existentes (e seus estados) são preservadas.
"""
from django.core.management.base import BaseCommand

from apps.products.models import Category

# Estilos masculinos de streetwear organizados por grupo
STYLES = {
    "Vestuário Superior": [
        "Camisetas", "Camisas", "Regatas", "Polos", "Camisetas Oversized",
        "Blusas de Frio", "Moletons", "Moletom com Capuz", "Jaquetas",
        "Corta-Vento", "Coletes",
    ],
    "Vestuário Inferior": [
        "Calças", "Jeans", "Joggers", "Calças Cargo", "Bermudas", "Shorts",
    ],
    "Conjuntos": [
        "Conjuntos", "Agasalhos",
    ],
    "Calçados": [
        "Tênis", "Chinelos", "Slides",
    ],
    "Acessórios de Cabeça": [
        "Bonés", "Toucas", "Gorros", "Bandanas",
    ],
    "Acessórios": [
        "Óculos", "Relógios", "Correntes", "Pulseiras", "Anéis",
        "Meias", "Cintos", "Luvas",
    ],
    "Bolsas": [
        "Mochilas", "Shoulder Bags", "Pochetes", "Carteiras",
    ],
    "Íntimo": [
        "Cuecas",
    ],
}


class Command(BaseCommand):
    help = "Cadastra os estilos masculinos como categorias (inativas por padrão)."

    def handle(self, *args, **options):
        created = 0
        for grupo, nomes in STYLES.items():
            for nome in nomes:
                _, was_created = Category.objects.get_or_create(
                    name=nome, defaults={"is_active": False, "description": grupo}
                )
                if was_created:
                    created += 1
        total = Category.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"{created} novo(s) estilo(s) cadastrado(s). Total de categorias: {total}."
        ))
