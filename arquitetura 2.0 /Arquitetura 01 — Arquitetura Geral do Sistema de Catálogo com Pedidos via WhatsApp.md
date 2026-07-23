Arquitetura 01 — Arquitetura Geral do Sistema de Catálogo com Pedidos via WhatsApp

Status: Aprovada

Objetivo: Definir a arquitetura geral do sistema, os componentes principais, as tecnologias adotadas e as decisões arquiteturais que servirão como base para todo o desenvolvimento do projeto.

1. Objetivo

Desenvolver um sistema de catálogo digital para venda de produtos físicos, com foco em uma loja regional, oferecendo uma experiência simples, rápida e otimizada para dispositivos móveis.

O sistema permitirá que clientes naveguem pelo catálogo, adicionem produtos ao carrinho, preencham seus dados e enviem automaticamente o pedido para o WhatsApp da loja.

O proprietário terá acesso a um painel administrativo exclusivo para gerenciamento dos produtos, pedidos e demais informações da loja.

2. Escopo do Sistema

O sistema contemplará:

Catálogo de produtos.
Pesquisa de produtos.
Carrinho de compras persistente.
Finalização do pedido.
Envio automático do pedido para o WhatsApp da loja.
Controle de estoque.
Cadastro de pedidos.
Área simplificada do cliente.
Avaliações de produtos.
Cupons de desconto.
Frete local.
Retirada na loja.
Painel administrativo exclusivo.

Não fazem parte desta versão:

Marketplace.
Múltiplas lojas.
Correios.
Melhor Envio.
Gateway de pagamento.
Aplicativo publicado na Play Store ou App Store.
3. Visão Geral da Arquitetura

O sistema será composto por um único projeto Django organizado como um Monólito Modular, separando claramente os módulos de negócio sem dividir a aplicação em múltiplos serviços.

Existirão dois ambientes principais.

Frontend Público

Responsável pela experiência do cliente.

Funções:

Navegação.
Catálogo.
Pesquisa.
Carrinho.
Finalização do pedido.
Envio do pedido para o WhatsApp.
Painel Administrativo

Responsável pelo gerenciamento da loja.

Funções:

Produtos.
Categorias.
Estoque.
Pedidos.
Cupons.
Clientes.
Avaliações.

O painel administrativo utilizará autenticação exclusiva para o proprietário da loja.

4. Tecnologias Adotadas
Backend
Python
Django
Banco de Dados
PostgreSQL
Servidor
Hostinger VPS
Ubuntu Linux
Gunicorn
Nginx
Frontend
HTML5
CSS3
JavaScript
Arquitetura
Monólito Modular
Responsividade
Mobile First
5. Componentes do Sistema

O sistema será dividido nos seguintes componentes principais:

Interface Pública
Painel Administrativo
Backend Django
Banco de Dados PostgreSQL
Serviço de Upload de Imagens
Serviço de Sessões
Integração com WhatsApp

Todos os componentes estarão hospedados na mesma infraestrutura da Hostinger VPS.

6. Fluxo Geral do Sistema

Fluxo simplificado:

Cliente

↓

Acessa o link da loja

↓

Visualiza catálogo

↓

Pesquisa produtos

↓

Seleciona produto

↓

Escolhe variações (cor e tamanho)

↓

Adiciona ao carrinho

↓

Carrinho permanece salvo automaticamente

↓

Finaliza o pedido

↓

Preenche os dados pessoais

↓

Escolhe a forma de entrega

Retirada na loja
Entrega

↓

O sistema gera automaticamente a mensagem do pedido

↓

Redireciona o cliente para o WhatsApp da loja

↓

Cliente envia a mensagem

↓

Administrador recebe o pedido

↓

Administrador altera o status do pedido no painel

↓

Cliente recebe automaticamente a atualização do pedido

7. Decisões Arquiteturais

As seguintes decisões são obrigatórias para esta versão do sistema.

Arquitetura
Monólito Modular.
Banco de Dados
PostgreSQL.
Hospedagem
Hostinger VPS.
Sistema Operacional
Ubuntu Linux.
Servidor Web
Nginx.
Servidor da Aplicação
Gunicorn.
Cache
Não será utilizado Redis nesta versão.
Processamento Assíncrono
Não será utilizado Celery nesta versão.
Containers
O projeto não utilizará Docker.
Responsividade
Mobile First.
Painel Administrativo
Interface totalmente separada da loja pública.
Carrinho
Persistência automática utilizando sessão/cookie seguro, sem exigir login.
Cliente
Não haverá cadastro tradicional.
Os dados pessoais serão solicitados apenas na finalização do pedido.
Após o primeiro preenchimento, os dados permanecerão disponíveis no mesmo dispositivo através da sessão persistente.
Produtos

Cada produto poderá possuir:

Nome.
Descrição.
Preço.
Estoque.
Categoria.
Até três imagens.
Cor.
Tamanho.
Estoque

O estoque será atualizado pelo administrador após o recebimento e confirmação do pedido.

Entrega

O sistema oferecerá duas modalidades:

Retirada na loja.
Entrega local.

Não haverá integração com transportadoras ou Correios.

Comunicação

Todos os pedidos serão enviados automaticamente para o WhatsApp da loja utilizando uma mensagem estruturada contendo todas as informações da compra.

8. Funcionalidades Principais
Cliente
Navegar pelo catálogo.
Pesquisar produtos.
Filtrar produtos.
Escolher tamanho.
Escolher cor.
Adicionar produtos ao carrinho.
Manter o carrinho salvo.
Finalizar o pedido.
Escolher retirada ou entrega.
Enviar automaticamente o pedido para o WhatsApp da loja.
Consultar pedidos realizados.
Avaliar produtos comprados.
Administrador
Gerenciar produtos.
Gerenciar categorias.
Gerenciar estoque.
Gerenciar pedidos.
Gerenciar clientes.
Gerenciar cupons.
Gerenciar avaliações.
Alterar o status dos pedidos.
9. Funcionalidades Fora do Escopo

Esta arquitetura não contempla:

Marketplace.
Múltiplos vendedores.
Correios.
Melhor Envio.
Gateway de pagamento.
Docker.
Redis.
Celery.
Microsserviços.
Aplicativo nativo Android.
Aplicativo nativo iOS.
10. Diretrizes Obrigatórias para o Cloud Code

Durante toda a implementação, o Cloud Code deverá respeitar obrigatoriamente as seguintes diretrizes:

Implementar o sistema utilizando Django com arquitetura de Monólito Modular.
Manter separação completa entre a loja pública e o painel administrativo.
Priorizar uma experiência Mobile First.
Não utilizar Docker, Redis ou Celery nesta versão.
Utilizar PostgreSQL como banco de dados principal.
Organizar o código em módulos independentes, preservando baixo acoplamento e alta coesão.
Implementar persistência do carrinho por sessão/cookie seguro.
Solicitar os dados do cliente apenas na finalização do pedido.
Implementar o envio automático do pedido para o WhatsApp da loja com uma mensagem estruturada e completa.
Desenvolver a solução preparada para futuras integrações, mantendo baixo acoplamento entre os módulos.
