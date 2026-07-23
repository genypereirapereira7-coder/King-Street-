Arquitetura 02 — Arquitetura dos Módulos do Sistema

Status: Aprovada

Objetivo: Definir a divisão lógica do sistema em módulos independentes, estabelecendo responsabilidades, limites de atuação e comunicação entre os componentes internos da aplicação.

1. Objetivo

Esta arquitetura define a organização interna do sistema utilizando uma abordagem baseada em módulos de negócio.

Cada módulo será responsável por um único domínio da aplicação, reduzindo o acoplamento entre funcionalidades e facilitando a manutenção, evolução e implementação pelo Cloud Code.

O sistema será desenvolvido como um único projeto Django utilizando a arquitetura Monólito Modular.

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
Finalização do Pedido
Cliente

Responsável pelas informações do comprador.

Módulos:

Clientes
Pedidos
Comercial

Responsável pelo processo comercial da loja.

Módulos:

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
Integração com WhatsApp
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

Finalização do Pedido

Responsável pela conclusão da compra.

Funções:

Receber os dados pessoais do cliente.
Receber o endereço de entrega.
Definir a forma de entrega.
Exibir o resumo do pedido.
Gerar o pedido.
Gerar automaticamente a mensagem para o WhatsApp da loja.
Redirecionar o cliente para o WhatsApp.

O cliente somente informará seus dados nesta etapa.

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

Pedido recebido.
Em preparação.
Saiu para entrega.
Entregue.
Cancelado.

Após alteração do status, o sistema poderá enviar automaticamente uma notificação ao cliente.

Cupons

Responsável pelos descontos promocionais.

Funções:

Validar cupons.
Aplicar descontos.
Controlar validade.
Controlar regras de utilização.
Ativar ou desativar cupons.
Dashboard

Responsável pela visão geral da administração.

Exibirá informações como:

Total de pedidos.
Pedidos em preparação.
Pedidos entregues.
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

Cliente

Poderá:

Visualizar avaliações.
Avaliar apenas produtos comprados.
Adicionar até três imagens em cada avaliação.
Administrador

Poderá:

Visualizar avaliações.
Ocultar avaliações.
Excluir avaliações.
Sessões

Responsável pela persistência da navegação do cliente.

Funções:

Manter o carrinho salvo.
Manter os dados do cliente no mesmo dispositivo.
Evitar novo preenchimento das informações em compras futuras.
Upload de Imagens

Responsável pelo armazenamento das imagens do sistema.

Funções:

Upload das imagens dos produtos.
Upload das imagens das avaliações.
Organização das imagens.
Associação das imagens aos respectivos registros.
Exclusão quando necessário.
Integração com WhatsApp

Responsável pelo envio do pedido para a loja.

Funções:

Montar automaticamente a mensagem do pedido.
Organizar os dados do cliente.
Organizar os produtos selecionados.
Informar forma de entrega.
Informar endereço quando necessário.
Redirecionar automaticamente o cliente para o WhatsApp da loja.
4. Comunicação Entre os Módulos

Fluxo principal:

Home

↓

Catálogo

↓

Produtos

↓

Carrinho

↓

Finalização do Pedido

↓

Pedidos

↓

Integração com WhatsApp

↓

Cliente envia o pedido

↓

Administrador recebe o pedido

Os módulos não deverão acessar diretamente dados internos uns dos outros.

Toda comunicação deverá ocorrer através das camadas de serviço definidas pelo backend.

5. Regras Arquiteturais

Todos os módulos deverão seguir obrigatoriamente as seguintes regras:

Cada módulo terá apenas uma responsabilidade.
Os módulos deverão possuir baixo acoplamento.
As regras de negócio permanecerão dentro do próprio módulo.
A comunicação entre módulos ocorrerá através de serviços internos.
Nenhum módulo poderá acessar diretamente a implementação interna de outro módulo.
O painel administrativo utilizará os mesmos módulos de negócio da loja pública, diferenciando apenas permissões e interfaces.
6. Organização Esperada pelo Cloud Code

Cada módulo deverá possuir sua própria estrutura interna, contendo os componentes necessários para seu funcionamento, como modelos, serviços, validações, rotas e demais elementos relacionados ao domínio.

Todos os novos módulos deverão seguir o mesmo padrão arquitetural estabelecido nesta documentação.

7. Diretrizes Obrigatórias

Durante toda a implementação, o Cloud Code deverá obrigatoriamente:

Implementar todos os módulos definidos nesta arquitetura.
Manter uma única responsabilidade para cada módulo.
Evitar duplicação de regras de negócio.
Compartilhar apenas contratos de comunicação entre módulos.
Manter separação completa entre o painel administrativo e a loja pública.
Implementar o envio estruturado dos pedidos para o WhatsApp.
Garantir que cada módulo possa evoluir independentemente sem impactar os demais.
Preservar a organização modular durante toda a evolução do sistema.
