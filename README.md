# 👑 King Street

Sistema de catálogo digital com pedidos via WhatsApp — Django (Monólito Modular),
tema preto, Mobile First, painel administrativo PWA.

> Construído seguindo as 6 arquiteturas aprovadas (ver `ARQUITETURA.md`).

## Como rodar (desenvolvimento)

```bash
# 1. Ativar o ambiente virtual
venv\Scripts\activate            # Windows

# 2. (opcional) copiar variáveis de ambiente
copy .env.example .env

# 3. Aplicar migrations e popular dados de demonstração
python manage.py migrate
python manage.py seed_demo

# 4. Subir o servidor
python manage.py runserver
```

- **Loja pública:** http://127.0.0.1:8000/
- **Painel administrativo:** http://127.0.0.1:8000/painel/
- **Login do painel (demo):** `admin` / `admin123`

## Estrutura (Monólito Modular)

```
config/            Configurações do projeto Django
apps/
  core/            Base compartilhada, PWA, filtros, erros
  products/        Categorias, produtos, imagens, variações + estoque
  customers/       Clientes (dados na finalização, sessão persistente)
  cart/            Carrinho por sessão + cupom
  coupons/         Cupons de desconto
  orders/          Pedidos, itens, histórico + integração WhatsApp
  reviews/         Avaliações (só quem comprou) + imagens
  store/           Loja pública (views/templates)
  dashboard/       Painel administrativo (PWA, mobile first)
templates/         Templates da loja, painel, PWA e erros
static/            CSS (tema preto), JS, ícones PWA
media/             Uploads (imagens de produtos e avaliações)
```

Cada módulo concentra sua regra de negócio na camada `services.py`
(as views apenas orquestram) — conforme a Arquitetura 06.

## Banco de dados

- **Desenvolvimento:** SQLite automático (nenhuma configuração necessária).
- **Produção (PostgreSQL):** preencha `DB_ENGINE`, `DB_NAME`, `DB_USER`,
  `DB_PASSWORD`, `DB_HOST`, `DB_PORT` no `.env`. As migrations são idênticas.

## Configuração da loja (`.env`)

| Variável         | Descrição                                             |
|------------------|-------------------------------------------------------|
| `STORE_NAME`     | Nome exibido na loja e no painel                      |
| `STORE_WHATSAPP` | WhatsApp da loja (só dígitos, DDI+DDD). Ex: `5511...` |
| `SECRET_KEY`     | Chave secreta (obrigatória em produção)               |
| `DEBUG`          | `True` em dev, `False` em produção                    |

## Tema (cores)

As cores ficam centralizadas em `static/css/theme.css`, no bloco `:root`.
O tema base é **preto**; o destaque (`--accent`) está como dourado provisório.
Quando as paletas forem definidas, basta alterar as variáveis — todo o sistema
se ajusta automaticamente.
