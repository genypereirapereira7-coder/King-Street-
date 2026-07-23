Arquitetura 01 — Arquitetura Geral do Sistema de E-commerce

Versão: 1.0
Status: Aprovada
Objetivo: Definir a arquitetura geral do sistema, os componentes principais, as tecnologias adotadas e as decisões arquiteturais que servirão como base para todo o desenvolvimento do projeto.

1. Objetivo

Desenvolver um sistema de e-commerce para venda de produtos físicos, com foco em uma loja regional, oferecendo uma experiência simples, rápida e otimizada para dispositivos móveis.

O sistema deverá permitir que clientes naveguem pelo catálogo, adicionem produtos ao carrinho sem necessidade de cadastro prévio, finalizem compras por PIX e acompanhem seus pedidos. O proprietário da loja terá acesso a um painel administrativo exclusivo para gerenciamento completo da operação.

2. Escopo do Sistema

O sistema contemplará:

Catálogo de produtos.
Pesquisa de produtos.
Carrinho de compras persistente.
Checkout simplificado.
Pagamento via PIX.
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
Integração com ERP.
Aplicativo publicado na Play Store ou App Store.
3. Visão Geral da Arquitetura

O sistema será composto por um único projeto Django organizado como um Monólito Modular, separando claramente os módulos de negócio sem dividir a aplicação em múltiplos serviços.

Existirão dois ambientes principais:

Frontend Público

Responsável pela experiência do cliente.

Funções:

Navegação.
Catálogo.
Pesquisa.
Carrinho.
Checkout.
Acompanhamento do pedido.

Painel Administrativo

Responsável pelo gerenciamento da loja.

Funções:

Produtos.
Categorias.
Estoque.
Pedidos.
Cupons.
Avaliações.
Configurações.

O painel administrativo será independente da interface pública, utilizando autenticação exclusiva para o proprietário da loja.

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
Serviço de Pagamentos (gateway a definir)
Serviço de Sessão do Cliente

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

Checkout

↓

Preenchimento dos dados pessoais

↓

Pagamento via PIX

↓

Confirmação automática do pagamento (via gateway)

↓

Pedido registrado

↓

Atualização automática do estoque

↓

Exibição da previsão de entrega

7. Decisões Arquiteturais

As seguintes decisões são obrigatórias para esta versão do sistema:

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
Login do Cliente
Não haverá cadastro prévio.
Os dados pessoais serão informados apenas durante o checkout.
Após o preenchimento, a sessão permanecerá ativa no mesmo dispositivo, evitando novo preenchimento em compras futuras.
Produtos

Cada produto poderá possuir:

Nome.
Descrição.
Preço.
Estoque.
Categoria.
Até 3 imagens.
Variações de cor.
Variações de tamanho.

Não haverá personalização por texto, imagem ou gravações.

Estoque

O estoque será atualizado automaticamente após a confirmação do pagamento.

Frete

Inicialmente haverá:

Entrega local.
Retirada na loja.

Não haverá integração com transportadoras ou Correios nesta versão.

8. Funcionalidades Principais

Cliente

Navegar pelo catálogo.
Pesquisar produtos.
Filtrar produtos.
Escolher tamanho.
Escolher cor.
Adicionar ao carrinho.
Manter carrinho salvo.
Finalizar compra.
Efetuar pagamento via PIX.
Visualizar previsão de entrega.
Consultar pedidos realizados.
Avaliar produtos comprados.

Administrador

Gerenciar produtos.
Gerenciar categorias.
Gerenciar estoque.
Gerenciar pedidos.
Gerenciar cupons.
Gerenciar avaliações.
Gerenciar configurações da loja.
9. Funcionalidades Fora do Escopo

Esta arquitetura não contempla:

Marketplace.
Múltiplos vendedores.
Correios.
Melhor Envio.
Integração com ERP.
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
Restringir autenticação ao painel administrativo e ao fluxo de checkout, sem exigir cadastro prévio para navegação.
Desenvolver a solução de forma preparada para futuras integrações (gateway de pagamento, frete e outros serviços), mantendo interfaces desacopladas.
