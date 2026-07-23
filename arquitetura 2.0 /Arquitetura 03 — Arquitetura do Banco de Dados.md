Arquitetura 03 — Arquitetura do Banco de Dados

Status: Aprovada

Objetivo: Definir a estrutura lógica do banco de dados, os relacionamentos entre as entidades, as regras de integridade e a organização das informações utilizadas pelo sistema de catálogo com pedidos via WhatsApp.

1. Objetivo

Esta arquitetura define como todas as informações do sistema serão armazenadas no PostgreSQL.

A modelagem seguirá princípios de normalização, integridade referencial, baixo acoplamento e consistência dos dados, garantindo facilidade de manutenção e evolução futura do sistema.

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

O SKU será utilizado exclusivamente para controle interno da loja.

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

Os dados serão preenchidos apenas na finalização do pedido.

Não haverá cadastro tradicional.

9. Carrinho

O carrinho será temporário.

Campos:

ID
Identificador da sessão
Produto
Quantidade
Data de criação

Após o envio do pedido para o WhatsApp, o carrinho será automaticamente esvaziado.

10. Pedidos

Cada pedido possuirá:

ID
Número do pedido
Cliente
Valor total
Forma de entrega
Status atual
Data do pedido

Status previstos:

Pedido recebido
Em preparação
Saiu para entrega
Entregue
Cancelado

O pedido será criado antes do redirecionamento para o WhatsApp, permitindo que o administrador acompanhe todo o processo dentro do painel.

11. Itens do Pedido

Cada pedido possuirá seus próprios itens.

Campos:

ID
Pedido
Produto
Variação do produto
Quantidade
Preço no momento do pedido

O preço será armazenado para preservar o histórico mesmo que o produto seja alterado futuramente.

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

Pedido recebido

↓

Em preparação

↓

Saiu para entrega

↓

Entregue

Nenhuma alteração de status deverá apagar registros anteriores.

13. Cupons

Cada cupom possuirá:

ID
Código
Tipo (Valor Fixo ou Percentual)
Valor
Data de início
Data de vencimento
Status (Ativo/Inativo)
Quantidade máxima de utilizações (opcional)

O administrador poderá ativar ou desativar cupons sem necessidade de exclusão.

14. Avaliações

Cada avaliação possuirá:

ID
Cliente
Produto
Nota
Comentário
Data da avaliação

Somente clientes que efetivamente realizaram um pedido contendo o produto poderão realizar avaliações.

15. Imagens das Avaliações

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

16. Relacionamentos Principais

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

Histórico do Pedido

Produtos

↓

Avaliações

↓

Imagens das Avaliações

Produtos

↓

Imagens dos Produtos

17. Regras de Integridade

O banco deverá garantir:

Produtos não poderão existir sem categoria.
Variações deverão pertencer obrigatoriamente a um produto.
Avaliações deverão estar vinculadas a um cliente e a um produto.
Imagens deverão pertencer obrigatoriamente ao seu registro principal.
Itens do pedido deverão armazenar o preço praticado no momento da compra.
O histórico dos pedidos nunca poderá ser removido automaticamente.
O estoque será controlado pelas variações dos produtos.
Um cliente somente poderá avaliar produtos presentes em seus pedidos.
18. Índices Recomendados

Criar índices para:

SKU
Nome do produto
Categoria
Status do pedido
Código do cupom
Telefone do cliente
Data do pedido

Esses índices deverão otimizar as consultas mais frequentes da aplicação.

19. Diretrizes Obrigatórias para o Cloud Code

Durante toda a implementação, o Cloud Code deverá obrigatoriamente:

Implementar todas as tabelas previstas nesta arquitetura.
Utilizar chaves estrangeiras em todos os relacionamentos.
Garantir integridade referencial entre todas as entidades.
Evitar duplicação de informações.
Manter histórico permanente dos pedidos.
Controlar estoque pelas variações dos produtos.
Armazenar imagens em tabelas independentes.
Preservar o preço histórico dos itens do pedido.
Utilizar PostgreSQL como banco de dados principal.
Criar o pedido antes do redirecionamento para o WhatsApp, garantindo o registro da operação no sistema.
