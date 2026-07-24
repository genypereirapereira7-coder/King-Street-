"""Catálogo de estilos masculinos (streetwear) usado para popular as categorias.

Fonte única da verdade: o comando `seed_styles` e a migração de dados
`0003_seed_styles` leem daqui. Para adicionar um novo estilo ao sistema,
basta incluí-lo na lista do grupo correspondente — o próximo deploy
cadastra os que faltarem (sempre inativos, o admin decide o que publicar).
"""

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


def iter_styles():
    """Gera pares (nome_do_estilo, grupo) na ordem do catálogo."""
    for grupo, nomes in STYLES.items():
        for nome in nomes:
            yield nome, grupo
