Arquitetura 05 — Arquitetura do Painel Administrativo

Status: Aprovada

Objetivo: Definir a estrutura, organização e funcionamento do painel administrativo, responsável pelo gerenciamento completo da loja.

1. Objetivo

O painel administrativo será o ambiente exclusivo utilizado pelo proprietário da loja para gerenciar toda a operação do sistema.

O painel deverá priorizar simplicidade, rapidez e facilidade de uso, permitindo que todas as tarefas diárias sejam realizadas com poucos cliques.

O sistema será otimizado para utilização em dispositivos móveis, podendo ser instalado como um aplicativo (PWA), sem necessidade de publicação na Play Store.

2. Acesso ao Painel

O acesso será restrito ao administrador.

Autenticação:

Usuário
Senha

Não haverá:

Login com Google.
Login com Facebook.
Múltiplos administradores.
Controle de permissões.
Controle de cargos.

Todo o painel será destinado exclusivamente ao proprietário da loja.

3. Dashboard

Ao acessar o painel, o administrador visualizará um resumo da operação da loja.

Serão exibidos:

Total de pedidos.
Pedidos do dia.
Produtos cadastrados.
Produtos com baixo estoque.
Últimos pedidos recebidos.

O dashboard deverá apresentar apenas informações relevantes para facilitar a gestão diária.

4. Gerenciamento de Produtos

O administrador poderá:

Cadastrar produtos.
Editar produtos.
Excluir produtos.
Ativar produtos.
Inativar produtos.

Cada produto poderá conter:

Nome.
Descrição.
Categoria.
Preço.
Cor.
Tamanho.
Quantidade em estoque.
Até três imagens.

Todas as alterações deverão refletir imediatamente na loja pública.

5. Gerenciamento de Categorias

O administrador poderá:

Criar categorias.
Editar categorias.
Excluir categorias.

As categorias serão utilizadas para organizar o catálogo.

6. Controle de Estoque

O estoque será controlado por variação de produto.

Cada combinação possuirá sua própria quantidade.

Exemplo:

Camiseta Branca

↓

P → 10 unidades

M → 5 unidades

G → 2 unidades

O administrador poderá alterar as quantidades diretamente pelo painel.

Quando uma variação atingir quantidade igual a zero, ela será identificada como Esgotada.

Quando todas as variações estiverem esgotadas, o produto será removido automaticamente do catálogo público.

7. Gerenciamento de Pedidos

Todos os pedidos recebidos serão exibidos no painel.

Cada pedido apresentará:

Número do pedido.
Nome do cliente.
Telefone.
Produtos solicitados.
Quantidade.
Valor total.
Forma de entrega.
Endereço completo (quando houver entrega).
Data do pedido.
Status atual.
Status dos Pedidos

O administrador poderá alterar manualmente o status do pedido.

Status disponíveis:

Pedido recebido.
Em preparação.
Saiu para entrega.
Entregue.
Cancelado.

Todas as alterações deverão ser registradas no histórico do pedido.

8. Comunicação com o Cliente

Cada pedido possuirá ações rápidas para facilitar o atendimento.

Botões disponíveis:

Abrir conversa no WhatsApp.
Compartilhar pedido no WhatsApp.
Copiar endereço completo.
Copiar telefone do cliente.

Essas ações deverão reduzir o tempo necessário para atender cada pedido.

9. Cadastro de Clientes

O painel manterá um histórico dos clientes.

Cada registro apresentará:

Nome.
Telefone.
Endereço.
Complemento.
Bairro.
Cidade.
CEP.
Total de pedidos.
Data do último pedido.

Também será disponibilizada a opção de copiar rapidamente o endereço completo do cliente.

10. Pesquisa

O painel deverá possuir pesquisa rápida para localizar:

Produtos.
Categorias.
Clientes.
Pedidos.

As pesquisas deverão apresentar resultados em tempo reduzido.

11. Upload de Imagens

O administrador poderá realizar upload de imagens diretamente pelo painel.

Regras:

Máximo de três imagens por produto.
Organização da ordem das imagens.
Exclusão de imagens quando necessário.
Atualização imediata na loja pública.
12. Responsividade

Todo o painel administrativo deverá seguir o conceito Mobile First.

A interface deverá funcionar corretamente em:

Smartphones.
Tablets.
Computadores.

O administrador deverá conseguir operar toda a loja utilizando apenas o celular.

13. Instalação como Aplicativo

O painel administrativo deverá permitir instalação como Progressive Web App (PWA).

Características:

Instalação diretamente pelo navegador.
Ícone na tela inicial do celular.
Acesso rápido.
Funcionamento semelhante a um aplicativo.

Não será necessária publicação na Play Store.

14. Regras Gerais

O painel deverá seguir obrigatoriamente as seguintes regras:

Apenas um administrador terá acesso.
Todas as alterações refletirão imediatamente na loja pública.
O estoque será atualizado por variações de produto.
Produtos inativos não aparecerão para os clientes.
Produtos totalmente esgotados serão removidos automaticamente do catálogo.
Todas as alterações de status dos pedidos serão registradas.
O painel deverá priorizar rapidez e simplicidade de uso.
15. Diretrizes Obrigatórias para o Cloud Code

Durante toda a implementação, o Cloud Code deverá obrigatoriamente:

Desenvolver um painel administrativo independente da loja pública.
Implementar autenticação exclusiva para o administrador.
Seguir o conceito Mobile First em todas as telas.
Permitir instalação como PWA.
Implementar pesquisa rápida em todos os módulos.
Atualizar automaticamente a loja pública após alterações administrativas.
Implementar ações rápidas para atendimento via WhatsApp.
Permitir cópia rápida de endereços e telefones.
Manter a interface simples, objetiva e otimizada para uso diário.
