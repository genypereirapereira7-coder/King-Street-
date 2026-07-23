Arquitetura 03 — Arquitetura do Banco de Dados

Versão: 1.0
Status: Aprovada
Objetivo: Definir a estrutura lógica do banco de dados, os relacionamentos entre as entidades, as regras de integridade e a organização das informações utilizadas pelo sistema de e-commerce.

1. Objetivo

Esta arquitetura define como todas as informações do sistema serão armazenadas no PostgreSQL.

A modelagem deverá seguir princípios de normalização, baixo acoplamento e integridade referencial, garantindo consistência dos dados, facilidade de manutenção e desempenho adequado para o porte do projeto.

2. Banco de Dados

Banco adotado:

PostgreSQL

Características obrigatórias:

Integridade referencial.
Chaves estrangeiras.
Índices para consultas frequentes.
Constraints de validação.
Datas de criação e atualização nos registros principais.
3. Estrutura Geral

O banco será dividido nos seguintes domínios:

Produtos
Categorias
Imagens dos Produtos
Variações dos Produtos
Clientes
Carrinho
Pedidos
Itens do Pedido
Histórico do Pedido
Pagamentos
Cupons
Avaliações
Imagens das Avaliações
4. Produtos

Cada produto possuirá:

ID
SKU
Nome
Descrição
Preço
Categoria
Status (Ativo/Inativo)
Data de criação
Data de atualização

O SKU será utilizado apenas para controle interno da loja.

5. Categorias

Cada categoria possuirá:

ID
Nome
Descrição
Status
Data de criação

Relacionamento:

Uma categoria poderá possuir vários produtos.

6. Imagens dos Produtos

Cada produto poderá possuir até três imagens.

Campos:

ID
Produto
Caminho da imagem
Ordem da imagem

Relacionamento:

Produto

↓

Imagens

(1:N)

7. Variações dos Produtos

As variações controlarão estoque por combinação de cor e tamanho.

Campos:

ID
Produto
Cor
Tamanho
Quantidade em estoque

Exemplo:

Produto

↓

Camiseta Básica

↓

Branca

↓

P

↓

10 unidades

Cada combinação possuirá seu próprio estoque.

8. Clientes

Cada cliente possuirá:

ID
Nome
Telefone
Endereço
Complemento
Bairro
Cidade
CEP
Data do primeiro pedido
Data da última compra

Os dados serão preenchidos durante o checkout.

Não haverá cadastro tradicional antes da compra.

9. Carrinho

O carrinho será temporário.

Campos:

ID
Identificador da sessão
Produto
Quantidade
Data de criação

Após a conclusão da compra, o carrinho será automaticamente esvaziado.

10. Pedidos

Cada pedido possuirá:

ID
Número do pedido
Cliente
Valor total
Forma de pagamento
Forma de entrega
Status atual
Data do pedido

Status previstos:

Aguardando pagamento
Pago
Em preparação
Saiu para entrega
Entregue
Cancelado
11. Itens do Pedido

Cada pedido possuirá seus próprios itens.

Campos:

ID
Pedido
Produto
Variação do produto
Quantidade
Preço no momento da compra

O preço será armazenado para preservar o histórico mesmo que o produto seja alterado posteriormente.

12. Histórico do Pedido

Toda alteração de status deverá ser registrada.

Campos:

ID
Pedido
Status anterior
Novo status
Data da alteração
Observação (opcional)

Exemplo:

Pedido

↓

Aguardando pagamento

↓

Pago

↓

Em preparação

↓

Saiu para entrega

↓

Entregue

Nenhuma alteração de status deverá apagar registros anteriores.

13. Pagamentos

Cada pagamento possuirá:

ID
Pedido
Tipo de pagamento
Valor
Status
Data da criação
Data da confirmação

Formas previstas:

PIX
Cartão

O gateway responsável será definido futuramente.

14. Cupons

Cada cupom possuirá:

ID
Código
Tipo
Valor
Data de início
Data de vencimento
Status (Ativo/Inativo)
Quantidade máxima de utilizações (opcional)

O administrador poderá ativar ou desativar cupons sem necessidade de exclusão.

15. Avaliações

Cada avaliação possuirá:

ID
Cliente
Produto
Nota
Comentário
Data da avaliação

Somente clientes que efetivamente compraram o produto poderão realizar avaliações.

16. Imagens das Avaliações

Cada avaliação poderá possuir até três imagens.

Campos:

ID
Avaliação
Caminho da imagem
Ordem da imagem

Relacionamento:

Avaliação

↓

Imagens

(1:N)

17. Relacionamentos Principais

Categoria

↓

Produtos

↓

Variações

↓

Itens do Pedido

↓

Pedidos

↓

Cliente

Pedidos

↓

Pagamentos

Pedidos

↓

Histórico do Pedido

Produtos

↓

Avaliações

↓

Imagens das Avaliações

Produtos

↓

Imagens dos Produtos

18. Regras de Integridade

O banco deverá garantir:

Produtos não poderão existir sem categoria.
Variações deverão pertencer a um produto.
Avaliações deverão estar vinculadas a um cliente e a um produto.
Imagens deverão pertencer obrigatoriamente ao seu registro principal.
Itens do pedido deverão armazenar o preço da compra.
O histórico dos pedidos nunca poderá ser removido automaticamente.
O estoque deverá ser controlado pelas variações do produto.
19. Índices Recomendados

Criar índices para:

SKU
Nome do produto
Categoria
Status do pedido
Código do cupom
Telefone do cliente
Data do pedido

Esses índices otimizarão as consultas mais frequentes da aplicação.

20. Diretrizes Obrigatórias para o Cloud Code

Durante toda a implementação, o Cloud Code deverá obrigatoriamente:

Implementar todas as tabelas previstas nesta arquitetura.
Utilizar chaves estrangeiras para todos os relacionamentos.
Garantir integridade referencial em todas as entidades.
Evitar duplicação de informações.
Manter histórico permanente dos pedidos.
Controlar estoque pelas variações de produto.
Armazenar imagens em tabelas independentes.
Preservar o preço histórico dos itens do pedido.
Utilizar PostgreSQL como banco principal.
