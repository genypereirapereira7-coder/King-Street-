Arquitetura 02 — Arquitetura dos Módulos do Sistema

Versão: 1.0
Status: Aprovada
Objetivo: Definir a divisão lógica do sistema em módulos independentes, estabelecendo responsabilidades, limites de atuação e comunicação entre os componentes internos da aplicação.

1. Objetivo

Esta arquitetura estabelece a organização interna do sistema utilizando uma abordagem baseada em módulos de negócio.

Cada módulo será responsável por um único domínio da aplicação, reduzindo o acoplamento entre funcionalidades e facilitando a manutenção, evolução e implementação pelo Cloud Code.

O sistema continuará sendo um único projeto Django (Monólito Modular), porém dividido em módulos bem definidos.

2. Estrutura Geral dos Módulos

O sistema será organizado em quatro grupos principais.

Loja Pública

Responsável por toda a experiência do cliente.

Módulos:

Home
Catálogo
Produtos
Pesquisa
Carrinho
Checkout
Cliente

Responsável pelas informações do comprador.

Módulos:

Clientes
Pedidos
Comercial

Responsável pelo processamento da compra.

Módulos:

Pagamentos
Cupons
Administração

Responsável pelo gerenciamento completo da loja.

Módulos:

Dashboard
Produtos
Categorias
Pedidos
Clientes
Cupons
Avaliações
Infraestrutura

Responsável pelo funcionamento interno do sistema.

Módulos:

Sessões
Upload de Imagens
3. Responsabilidade de Cada Módulo
Home

Responsável pela página inicial da loja.

Funções:

Banner principal.
Produtos em destaque.
Acesso ao catálogo.
Exibição das avaliações.
Navegação para as demais áreas da loja.
Catálogo

Responsável pela listagem dos produtos.

Funções:

Exibir produtos.
Paginação.
Ordenação.
Aplicação de filtros.
Navegação entre categorias.
Produtos

Responsável pelas informações dos produtos.

Cada produto possuirá:

Nome.
Descrição.
Categoria.
Preço.
Quantidade em estoque.
Até três imagens.
Cor.
Tamanho.
Pesquisa

Responsável pela busca de produtos.

Permitirá pesquisa por:

Nome.
Categoria.
Cor.
Tamanho.
Faixa de preço.
Carrinho

Responsável pelo gerenciamento do carrinho.

Funções:

Adicionar produtos.
Remover produtos.
Alterar quantidade.
Atualizar valores.
Aplicar cupons.
Manter o carrinho salvo automaticamente utilizando sessão persistente.

O carrinho poderá ser acessado por qualquer ponto da navegação da loja.

Checkout

Responsável pela finalização da compra.

Funções:

Receber dados pessoais.
Receber endereço de entrega.
Definir forma de entrega.
Selecionar forma de pagamento.
Exibir resumo da compra.
Criar o pedido.

O cliente somente informará seus dados durante esta etapa.

Não haverá cadastro tradicional antes da compra.

Clientes

Responsável pelos dados dos compradores.

Armazenará:

Nome.
Telefone.
Endereço.
Complemento.
Bairro.
Cidade.
CEP.
Histórico de pedidos.

Os dados serão preenchidos apenas na primeira compra e reutilizados automaticamente nas próximas compras realizadas no mesmo dispositivo através da sessão persistente.

Pedidos

Responsável por todo o ciclo do pedido.

Funções:

Criar pedido.
Gerar número do pedido.
Registrar histórico.
Controlar status.

Status previstos:

Aguardando pagamento.
Pago.
Em preparação.
Saiu para entrega.
Entregue.
Cancelado.

Após alteração do status para Entregue, o sistema enviará automaticamente uma notificação ao cliente.

Pagamentos

Responsável pelo processamento dos pagamentos.

Formas aceitas:

PIX.
Cartão.

Funções:

Gerar cobrança.
Receber confirmação do gateway (a ser definido).
Atualizar automaticamente o status do pedido após confirmação do pagamento.
Cupons

Responsável pelos descontos promocionais.

Funções:

Validar cupons.
Aplicar descontos.
Controlar validade.
Controlar regras de utilização.
Dashboard

Responsável pela visão geral da administração.

Exibirá informações como:

Total de pedidos.
Pedidos pendentes.
Pedidos pagos.
Produtos mais vendidos.
Indicadores básicos da operação.
Categorias

Responsável pela organização dos produtos.

Funções:

Criar categorias.
Editar categorias.
Excluir categorias.
Organizar a navegação do catálogo.
Avaliações

Responsável pelas avaliações dos produtos.

Cliente:

Visualizar avaliações.
Avaliar apenas produtos comprados.

Administrador:

Visualizar avaliações.
Ocultar avaliações.
Excluir avaliações.
Sessões

Responsável pela persistência da navegação do cliente.

Funções:

Manter o carrinho salvo.
Manter os dados do cliente no mesmo dispositivo.
Evitar novo preenchimento de informações em compras futuras.
Upload de Imagens

Responsável pelo armazenamento das imagens dos produtos.

Funções:

Upload.
Organização.
Associação das imagens aos produtos.
Exclusão de imagens quando necessário.
4. Comunicação Entre os Módulos

A comunicação seguirá responsabilidades bem definidas.

Fluxo principal:

Home

↓

Catálogo

↓

Produtos

↓

Carrinho

↓

Checkout

↓

Pagamentos

↓

Pedidos

↓

Cliente recebe confirmação

Os módulos não deverão acessar diretamente dados internos uns dos outros.

Toda comunicação deverá ocorrer através das camadas de serviço definidas pelo backend.

5. Regras Arquiteturais

Todos os módulos deverão seguir as seguintes regras:

Cada módulo terá uma única responsabilidade.
Os módulos deverão possuir baixo acoplamento.
As regras de negócio permanecerão dentro do próprio módulo.
A comunicação entre módulos ocorrerá por serviços internos.
Nenhum módulo poderá acessar diretamente a implementação interna de outro módulo.
O painel administrativo utilizará os mesmos módulos de negócio da loja pública, diferenciando apenas permissões e interfaces.
6. Organização Esperada pelo Cloud Code

Cada módulo deverá possuir estrutura própria e independente, contendo seus componentes de domínio (modelos, serviços, validações, rotas e demais elementos necessários), mantendo padronização em todo o projeto.

Novos módulos deverão seguir a mesma organização estabelecida nesta arquitetura, preservando a separação de responsabilidades e evitando duplicação de regras de negócio.

7. Diretrizes Obrigatórias

Durante toda a implementação, o Cloud Code deverá seguir obrigatoriamente:

Implementar todos os módulos descritos nesta arquitetura.
Não concentrar regras de negócio em um único módulo.
Reutilizar componentes sempre que possível.
Compartilhar apenas contratos de comunicação entre módulos.
Manter o painel administrativo separado da interface pública.
Garantir que cada módulo possa evoluir independentemente sem impactar os demais.
