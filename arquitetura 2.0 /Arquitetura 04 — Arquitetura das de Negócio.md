Arquitetura 04 — Arquitetura das Regras de Negócio

Status: Aprovada

Objetivo: Definir todas as regras de funcionamento do sistema, estabelecendo como cada funcionalidade deverá se comportar durante a operação da loja.

1. Objetivo

Esta arquitetura define todas as regras de negócio que deverão ser implementadas pelo Cloud Code.

Nenhuma funcionalidade poderá ser desenvolvida ignorando as regras estabelecidas neste documento.

As regras aqui descritas possuem prioridade sobre decisões de implementação.

2. Produtos
Cadastro

Cada produto deverá possuir obrigatoriamente:

Nome
Descrição
Categoria
Preço
Cor
Tamanho
Até três imagens
Quantidade em estoque
Status
Status do Produto

O produto poderá possuir apenas dois estados:

Ativo
Inativo

Produtos inativos não deverão aparecer no catálogo da loja.

Estoque

O sistema utilizará um controle de estoque simples.

Cada combinação de cor e tamanho possuirá sua própria quantidade disponível.

Exemplo:

Camiseta Branca - P → 5 unidades

Camiseta Branca - M → 8 unidades

Camiseta Preta - G → 2 unidades

Produto Esgotado

Quando uma variação atingir quantidade igual a zero:

A variação deverá aparecer como Esgotada.

Quando todas as variações de um produto estiverem esgotadas:

O produto deverá ser removido automaticamente do catálogo público.
Exclusão de Produtos

O administrador poderá excluir produtos.

Caso o produto já tenha sido utilizado em pedidos anteriores, sua exclusão não poderá comprometer o histórico dos pedidos registrados no sistema.

3. Carrinho

O carrinho deverá funcionar através de sessão persistente.

Funções:

Adicionar produtos.
Remover produtos.
Alterar quantidade.
Atualizar valores automaticamente.

O cliente não poderá adicionar quantidade superior ao estoque disponível.

Persistência

O carrinho permanecerá salvo enquanto o cliente permanecer utilizando o mesmo dispositivo e não concluir o envio do pedido.

Após o pedido ser gerado e o cliente ser redirecionado ao WhatsApp da loja, o carrinho será automaticamente esvaziado.

4. Cliente

Não existirá cadastro tradicional.

O cliente apenas informará seus dados durante a finalização do pedido.

Serão solicitados:

Nome
Telefone
Endereço (quando necessário)
Complemento
Bairro
Cidade
CEP

Após o primeiro preenchimento, essas informações permanecerão armazenadas no mesmo dispositivo para agilizar futuras compras.

5. Pedido

O pedido será criado automaticamente antes do redirecionamento para o WhatsApp.

O sistema deverá registrar:

Cliente
Produtos
Quantidades
Variações
Valor total
Forma de entrega
Data

Após a criação do pedido, o sistema deverá gerar automaticamente uma mensagem estruturada contendo todas essas informações e abrir o WhatsApp da loja.

Caso o cliente feche o WhatsApp sem enviar a mensagem, nenhuma ação adicional será executada pelo sistema. O pedido permanecerá registrado.

6. Forma de Entrega

O sistema oferecerá apenas duas opções:

Retirada na loja
Entrega local

Não haverá integração com transportadoras.

Não haverá integração com os Correios.

A logística será totalmente administrada pelo proprietário da loja.

7. Administração dos Pedidos

Todos os pedidos ficarão disponíveis no painel administrativo.

O administrador poderá visualizar:

Dados do cliente
Produtos
Quantidades
Endereço
Valor total
Data do pedido

Também poderá alterar manualmente o status do pedido.

Status do Pedido

Os status disponíveis serão:

Pedido recebido
Em preparação
Saiu para entrega
Entregue
Cancelado

Toda alteração deverá ser registrada no histórico do pedido.

8. Sessões

O sistema utilizará sessão persistente para melhorar a experiência do cliente.

Serão mantidos:

Carrinho
Dados pessoais preenchidos anteriormente

As informações permanecerão disponíveis enquanto os dados do navegador forem preservados no mesmo dispositivo.

9. Pesquisa

A pesquisa permitirá localizar produtos por:

Nome
Categoria
Cor
Tamanho

Os resultados deverão ser apresentados em tempo de resposta reduzido, priorizando a experiência do usuário.

10. Imagens

Cada produto poderá possuir até três imagens.

As imagens deverão ser exibidas na ordem definida pelo administrador.

O sistema deverá impedir o envio de quantidade superior ao limite estabelecido.

11. Painel Administrativo

O painel administrativo será exclusivo do proprietário da loja.

Através dele será possível:

Gerenciar produtos.
Gerenciar categorias.
Gerenciar estoque.
Gerenciar pedidos.
Gerenciar clientes.

Todas as alterações realizadas no painel deverão refletir imediatamente na loja pública.

12. Regras Gerais

O sistema deverá seguir obrigatoriamente as seguintes regras:

Não permitir produtos com estoque negativo.
Não permitir adicionar ao carrinho quantidade superior ao estoque disponível.
Produtos inativos não poderão ser exibidos.
Produtos totalmente esgotados deverão ser removidos automaticamente do catálogo.
Cada variação possuirá controle individual de estoque.
O pedido será criado antes da abertura do WhatsApp.
O carrinho será limpo automaticamente após o redirecionamento para o WhatsApp.
O histórico dos pedidos deverá ser preservado permanentemente.
Os dados do cliente deverão permanecer disponíveis no mesmo dispositivo para futuras compras.
13. Diretrizes Obrigatórias para o Cloud Code

Durante toda a implementação, o Cloud Code deverá obrigatoriamente:

Implementar todas as regras descritas nesta arquitetura.
Centralizar as regras de negócio na camada de serviços do backend.
Garantir que nenhuma regra crítica fique apenas no frontend.
Validar todas as operações também no servidor.
Preservar o histórico dos pedidos.
Controlar o estoque por variações de produto.
Sincronizar automaticamente o catálogo conforme o estoque disponível.
Gerar o pedido antes do redirecionamento ao WhatsApp.
Limpar automaticamente o carrinho após o redirecionamento para o WhatsApp.
