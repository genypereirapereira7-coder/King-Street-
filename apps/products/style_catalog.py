"""Catálogo de estilos masculinos (streetwear) usado para popular as categorias.

Fonte única da verdade: o comando `seed_styles` e a migração de dados
`0003_seed_styles` leem daqui. Para adicionar um novo estilo ao sistema,
basta incluí-lo na lista do grupo correspondente — o próximo deploy
cadastra os que faltarem (sempre inativos, o admin decide o que publicar).

Nomes repetidos são ignorados automaticamente (a categoria é criada só se
ainda não existir pelo nome).
"""

STYLES = {
    "Vestuário Superior": [
        "Camisetas", "Camiseta básica", "Camiseta gola V", "Camiseta oversized",
        "Camisetas Oversized", "Camiseta estampada", "Camisas", "Regatas", "Regata",
        "Polos", "Camisa polo", "Camisa social", "Camisa de linho", "Camisa xadrez",
        "Camisa jeans", "Camisa cubana", "Camisa manga longa lisa",
        "Blusas de Frio", "Blusa gola alta", "Moletons", "Moletom careca",
        "Moletom com Capuz", "Suéter", "Cardigã",
    ],
    "Casacos & Jaquetas": [
        "Jaquetas", "Jaqueta jeans", "Jaqueta bomber", "Jaqueta de couro",
        "Jaqueta corta-vento", "Corta-Vento", "Jaqueta puffer", "Jaqueta college",
        "Parka", "Blazer", "Terno", "Sobretudo", "Trench coat", "Coletes", "Colete",
    ],
    "Vestuário Inferior": [
        "Calças", "Calça jeans reta", "Calça jeans skinny", "Calça jeans wide leg",
        "Jeans", "Calça de sarja", "Calça chino", "Calça social", "Calça cargo",
        "Calças Cargo", "Calça de moletom", "Joggers", "Jogger",
        "Bermudas", "Bermuda jeans", "Bermuda de sarja", "Bermuda de moletom",
        "Shorts", "Short esportivo", "Short de banho", "Sunga",
    ],
    "Conjuntos": [
        "Conjuntos", "Agasalhos",
    ],
    "Calçados": [
        "Tênis", "Tênis branco casual", "Tênis de corrida", "Tênis de skate",
        "Tênis chunky", "Sapatênis", "Mocassim", "Sapato oxford", "Sapato derby",
        "Bota coturno", "Bota chelsea", "Bota Timberland", "Sandália", "Papete",
        "Chinelos", "Chinelo", "Slides", "Crocs",
    ],
    "Acessórios de Cabeça": [
        "Bonés", "Boné aba curva", "Boné aba reta", "Boné trucker", "Bucket hat",
        "Toucas", "Gorros", "Gorro", "Bandanas", "Chapéu fedora", "Chapéu panamá",
    ],
    "Acessórios": [
        "Óculos", "Óculos de sol", "Relógios", "Relógio", "Correntes", "Corrente",
        "Colar", "Pulseiras", "Pulseira", "Anéis", "Anel", "Brinco",
        "Cintos", "Cinto de couro", "Cinto de lona", "Cachecol", "Luvas",
        "Gravata", "Gravata borboleta", "Suspensórios", "Lenço de bolso", "Abotoaduras",
    ],
    "Bolsas": [
        "Mochilas", "Mochila", "Shoulder Bags", "Bolsa transversal",
        "Pochetes", "Pochete", "Carteiras", "Carteira",
    ],
    "Íntimo & Meias": [
        "Cuecas", "Cueca boxer", "Cueca slip", "Samba-canção", "Regata interna",
        "Meias", "Meia soquete", "Meia cano médio", "Meia cano alto",
        "Meia esportiva", "Meia social",
    ],
    "Cuidados & Beleza": [
        "Corte de cabelo", "Barba aparada", "Perfume", "Desodorante",
        "Hidratante", "Protetor solar",
    ],
}


def iter_styles():
    """Gera pares (nome_do_estilo, grupo) na ordem do catálogo, sem repetir nomes."""
    vistos = set()
    for grupo, nomes in STYLES.items():
        for nome in nomes:
            if nome in vistos:
                continue
            vistos.add(nome)
            yield nome, grupo
