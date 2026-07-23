# 👑 King Street — Documentação de Arquitetura

> Sistema de Catálogo Digital com Pedidos via WhatsApp
> Documento vivo — atualizado conforme as partes forem enviadas.

## ✅ Status: SISTEMA CONSTRUÍDO (build inicial concluído)

Implementado em Django 6 seguindo as 6 arquiteturas. Ver `README.md` para rodar.
Login painel (demo): `admin` / `admin123`. Cores em `static/css/theme.css` (paletas ainda pendentes).

## Diretrizes Globais (definidas pelo cliente)

- **Front-end:** tema **preto (dark/black)** como base.
- **Paletas de cores:** *aguardando envio* 🎨
- **Modo de trabalho:** armazenar todas as partes; **só construir quando o cliente disser "cria"**.

---

## Índice de Arquiteturas

| Nº | Título | Status |
|----|--------|--------|
| 01 | Arquitetura Geral do Sistema de Catálogo com Pedidos via WhatsApp | ✅ Aprovada |
| 02 | Arquitetura dos Módulos do Sistema | ✅ Aprovada |
| 03 | Arquitetura do Banco de Dados | ✅ Aprovada |
| 04 | Arquitetura das Regras de Negócio | ✅ Aprovada |
| 05 | Arquitetura do Painel Administrativo | ✅ Aprovada |
| 06 | Arquitetura de Desenvolvimento e Padrões do Projeto | ✅ Aprovada |

---

## Arquitetura 01 — Arquitetura Geral do Sistema de Catálogo com Pedidos via WhatsApp

**Status:** Aprovada

**Objetivo:** Definir a arquitetura geral do sistema, os componentes principais, as tecnologias adotadas e as decisões arquiteturais que servirão como base para todo o desenvolvimento do projeto.

### 1. Objetivo
Sistema de **catálogo digital** para venda de produtos físicos, foco em **loja regional**, experiência simples, rápida e **otimizada para mobile**.
Cliente navega no catálogo, adiciona ao carrinho, preenche dados e o pedido é enviado automaticamente para o **WhatsApp da loja**.
Proprietário tem **painel administrativo exclusivo** para gerenciar produtos, pedidos e informações da loja.

### 2. Escopo do Sistema
**Contempla:** catálogo de produtos, pesquisa, carrinho persistente, finalização de pedido, envio automático ao WhatsApp, controle de estoque, cadastro de pedidos, área simplificada do cliente, avaliações de produtos, cupons de desconto, frete local, retirada na loja, painel administrativo exclusivo.

**NÃO contempla nesta versão:** Marketplace, múltiplas lojas, Correios, Melhor Envio, gateway de pagamento, app publicado na Play Store/App Store.

### 3. Visão Geral da Arquitetura
- Projeto único **Django** — **Monólito Modular** (módulos de negócio separados, sem múltiplos serviços).
- **Dois ambientes principais:**
  - **Frontend Público** (cliente): navegação, catálogo, pesquisa, carrinho, finalização, envio ao WhatsApp.
  - **Painel Administrativo** (loja): produtos, categorias, estoque, pedidos, cupons, clientes, avaliações.
  - Painel usa **autenticação exclusiva do proprietário**.

### 4. Tecnologias Adotadas
- **Backend:** Python, Django
- **Banco de Dados:** PostgreSQL
- **Servidor:** Hostinger VPS, Ubuntu Linux, Gunicorn, Nginx
- **Frontend:** HTML5, CSS3, JavaScript
- **Arquitetura:** Monólito Modular
- **Responsividade:** Mobile First

### 5. Componentes do Sistema
Interface Pública · Painel Administrativo · Backend Django · Banco de Dados PostgreSQL · Serviço de Upload de Imagens · Serviço de Sessões · Integração com WhatsApp.
*Todos hospedados na mesma infraestrutura Hostinger VPS.*

### 6. Fluxo Geral do Sistema
Cliente → acessa link → visualiza catálogo → pesquisa → seleciona produto → escolhe variações (cor/tamanho) → adiciona ao carrinho → carrinho salvo automaticamente → finaliza pedido → preenche dados pessoais → escolhe entrega (**Retirada na loja** ou **Entrega**) → sistema gera mensagem do pedido → redireciona para WhatsApp da loja → cliente envia → admin recebe → admin altera status no painel → cliente recebe atualização automática.

### 7. Decisões Arquiteturais (obrigatórias)
- **Arquitetura:** Monólito Modular
- **Banco:** PostgreSQL
- **Hospedagem:** Hostinger VPS · **SO:** Ubuntu Linux · **Web:** Nginx · **App:** Gunicorn
- **Cache:** SEM Redis nesta versão
- **Assíncrono:** SEM Celery nesta versão
- **Containers:** SEM Docker
- **Responsividade:** Mobile First
- **Painel Admin:** interface totalmente separada da loja pública
- **Carrinho:** persistência automática via sessão/cookie seguro, **sem login**
- **Cliente:** sem cadastro tradicional; dados solicitados só na finalização; após 1º preenchimento, dados ficam disponíveis no mesmo dispositivo via sessão persistente
- **Produtos** podem ter: Nome, Descrição, Preço, Estoque, Categoria, até **3 imagens**, Cor, Tamanho
- **Estoque:** atualizado pelo admin após recebimento e confirmação do pedido
- **Entrega:** Retirada na loja · Entrega local (sem transportadoras/Correios)
- **Comunicação:** todos os pedidos enviados automaticamente ao WhatsApp com mensagem estruturada e completa

### 8. Funcionalidades Principais
**Cliente:** navegar, pesquisar, filtrar, escolher tamanho, escolher cor, adicionar ao carrinho, manter carrinho salvo, finalizar pedido, escolher retirada ou entrega, enviar pedido ao WhatsApp, consultar pedidos realizados, avaliar produtos comprados.
**Administrador:** gerenciar produtos, categorias, estoque, pedidos, clientes, cupons, avaliações, alterar status dos pedidos.

### 9. Fora do Escopo
Marketplace · Múltiplos vendedores · Correios · Melhor Envio · Gateway de pagamento · Docker · Redis · Celery · Microsserviços · App nativo Android · App nativo iOS.

### 10. Diretrizes Obrigatórias para o Cloud Code
1. Django com arquitetura Monólito Modular.
2. Separação completa entre loja pública e painel administrativo.
3. Priorizar experiência Mobile First.
4. NÃO usar Docker, Redis ou Celery nesta versão.
5. PostgreSQL como banco principal.
6. Código em módulos independentes — baixo acoplamento, alta coesão.
7. Persistência do carrinho por sessão/cookie seguro.
8. Dados do cliente solicitados apenas na finalização.
9. Envio automático do pedido ao WhatsApp com mensagem estruturada e completa.
10. Solução preparada para futuras integrações, mantendo baixo acoplamento.

---

## Arquitetura 02 — Arquitetura dos Módulos do Sistema

**Status:** Aprovada

**Objetivo:** Definir a divisão lógica do sistema em módulos independentes, estabelecendo responsabilidades, limites de atuação e comunicação entre os componentes internos da aplicação.

### 1. Objetivo
Organização interna baseada em **módulos de negócio**. Cada módulo responsável por **um único domínio**, reduzindo acoplamento e facilitando manutenção. Único projeto Django — **Monólito Modular**.

### 2. Estrutura Geral dos Módulos (4 grupos)
- **Loja Pública** (experiência do cliente): Home · Catálogo · Produtos · Pesquisa · Carrinho · Finalização do Pedido
- **Cliente** (informações do comprador): Clientes · Pedidos
- **Comercial** (processo comercial): Cupons
- **Administração** (gerenciamento da loja): Dashboard · Produtos · Categorias · Pedidos · Clientes · Cupons · Avaliações
- **Infraestrutura** (funcionamento interno): Sessões · Upload de Imagens · Integração com WhatsApp

### 3. Responsabilidade de Cada Módulo
- **Home:** banner principal, produtos em destaque, acesso ao catálogo, exibição de avaliações, navegação.
- **Catálogo:** exibir produtos, paginação, ordenação, filtros, navegação entre categorias.
- **Produtos:** Nome, Descrição, Categoria, Preço, Quantidade em estoque, até 3 imagens, Cor, Tamanho.
- **Pesquisa:** busca por Nome, Categoria, Cor, Tamanho, Faixa de preço.
- **Carrinho:** adicionar/remover produtos, alterar quantidade, atualizar valores, aplicar cupons, manter salvo via sessão persistente; acessível de qualquer ponto da loja.
- **Finalização do Pedido:** receber dados pessoais e endereço, definir forma de entrega, exibir resumo, gerar pedido, gerar mensagem do WhatsApp, redirecionar. *Dados só informados nesta etapa; sem cadastro tradicional antes da compra.*
- **Clientes:** armazena Nome, Telefone, Endereço, Complemento, Bairro, Cidade, CEP, Histórico de pedidos. Dados preenchidos na 1ª compra e reutilizados no mesmo dispositivo via sessão persistente.
- **Pedidos:** criar pedido, gerar número, registrar histórico, controlar status. **Status:** Pedido recebido · Em preparação · Saiu para entrega · Entregue · Cancelado. Após mudança de status, pode notificar cliente automaticamente.
- **Cupons:** validar, aplicar descontos, controlar validade e regras de utilização, ativar/desativar.
- **Dashboard:** total de pedidos, pedidos em preparação, entregues, produtos mais vendidos, indicadores básicos.
- **Categorias:** criar, editar, excluir, organizar navegação do catálogo.
- **Avaliações:** Cliente → visualizar, avaliar apenas produtos comprados, adicionar até 3 imagens por avaliação. Admin → visualizar, ocultar, excluir.
- **Sessões:** manter carrinho salvo, manter dados do cliente no mesmo dispositivo, evitar novo preenchimento em compras futuras.
- **Upload de Imagens:** upload de imagens de produtos e avaliações, organização, associação aos registros, exclusão quando necessário.
- **Integração com WhatsApp:** montar mensagem do pedido, organizar dados do cliente e produtos, informar forma de entrega e endereço quando necessário, redirecionar automaticamente para o WhatsApp da loja.

### 4. Comunicação Entre os Módulos
Fluxo principal: Home → Catálogo → Produtos → Carrinho → Finalização do Pedido → Pedidos → Integração com WhatsApp → cliente envia → admin recebe.
- Módulos **não** acessam diretamente dados internos uns dos outros.
- Toda comunicação ocorre pelas **camadas de serviço** definidas pelo backend.

### 5. Regras Arquiteturais
- Cada módulo tem **apenas uma responsabilidade**.
- **Baixo acoplamento** entre módulos.
- Regras de negócio ficam **dentro do próprio módulo**.
- Comunicação entre módulos via **serviços internos**.
- Nenhum módulo acessa a implementação interna de outro.
- Painel admin usa os **mesmos módulos de negócio** da loja pública, diferenciando apenas **permissões e interfaces**.

### 6. Organização Esperada pelo Cloud Code
Cada módulo com sua própria estrutura interna (modelos, serviços, validações, rotas e demais elementos do domínio). Novos módulos seguem o mesmo padrão.

### 7. Diretrizes Obrigatórias
1. Implementar todos os módulos definidos.
2. Manter única responsabilidade por módulo.
3. Evitar duplicação de regras de negócio.
4. Compartilhar apenas contratos de comunicação entre módulos.
5. Separação completa entre painel admin e loja pública.
6. Implementar envio estruturado dos pedidos ao WhatsApp.
7. Garantir que cada módulo evolua independentemente.
8. Preservar a organização modular durante toda a evolução.

---

## Arquitetura 03 — Arquitetura do Banco de Dados

**Status:** Aprovada

**Objetivo:** Definir a estrutura lógica do banco de dados, relacionamentos entre entidades, regras de integridade e organização das informações.

### 1. Objetivo
Todas as informações armazenadas no **PostgreSQL**. Modelagem com normalização, integridade referencial, baixo acoplamento e consistência.

### 2. Banco de Dados
**PostgreSQL.** Características obrigatórias: integridade referencial, chaves estrangeiras, índices para consultas frequentes, constraints de validação, datas de criação e atualização nos registros principais.

### 3. Estrutura Geral (domínios/tabelas)
Produtos · Categorias · Imagens dos Produtos · Variações dos Produtos · Clientes · Carrinho · Pedidos · Itens do Pedido · Histórico do Pedido · Cupons · Avaliações · Imagens das Avaliações.

### 4. Produtos
Campos: ID, SKU, Nome, Descrição, Preço, Categoria, Status (Ativo/Inativo), Data de criação, Data de atualização.
*SKU é exclusivo para controle interno da loja.*

### 5. Categorias
Campos: ID, Nome, Descrição, Status, Data de criação.
Relacionamento: Categoria (1) → Produtos (N).

### 6. Imagens dos Produtos
Até **3 imagens** por produto. Campos: ID, Produto, Caminho da imagem, Ordem da imagem. Relacionamento: Produto → Imagens (1:N).

### 7. Variações dos Produtos
Controlam **estoque por combinação de cor e tamanho**. Campos: ID, Produto, Cor, Tamanho, Quantidade em estoque.
*Cada combinação (ex: Camiseta Básica / Branca / P → 10 un.) tem seu próprio estoque.*

### 8. Clientes
Campos: ID, Nome, Telefone, Endereço, Complemento, Bairro, Cidade, CEP, Data do primeiro pedido, Data da última compra.
*Dados preenchidos apenas na finalização do pedido; sem cadastro tradicional.*

### 9. Carrinho (temporário)
Campos: ID, Identificador da sessão, Produto, Quantidade, Data de criação.
*Após envio do pedido ao WhatsApp, o carrinho é esvaziado automaticamente.*

### 10. Pedidos
Campos: ID, Número do pedido, Cliente, Valor total, Forma de entrega, Status atual, Data do pedido.
**Status:** Pedido recebido · Em preparação · Saiu para entrega · Entregue · Cancelado.
*Pedido criado ANTES do redirecionamento ao WhatsApp, para o admin acompanhar no painel.*

### 11. Itens do Pedido
Campos: ID, Pedido, Produto, Variação do produto, Quantidade, **Preço no momento do pedido**.
*Preço armazenado para preservar o histórico mesmo se o produto mudar depois.*

### 12. Histórico do Pedido
Toda alteração de status registrada. Campos: ID, Pedido, Status anterior, Novo status, Data da alteração, Observação (opcional).
*Nenhuma alteração de status apaga registros anteriores.*

### 13. Cupons
Campos: ID, Código, Tipo (Valor Fixo ou Percentual), Valor, Data de início, Data de vencimento, Status (Ativo/Inativo), Quantidade máxima de utilizações (opcional).
*Admin pode ativar/desativar sem excluir.*

### 14. Avaliações
Campos: ID, Cliente, Produto, Nota, Comentário, Data da avaliação.
*Só clientes que realizaram pedido contendo o produto podem avaliar.*

### 15. Imagens das Avaliações
Até **3 imagens** por avaliação. Campos: ID, Avaliação, Caminho da imagem, Ordem da imagem. Relacionamento: Avaliação → Imagens (1:N).

### 16. Relacionamentos Principais
- Categoria → Produtos → Variações → Itens do Pedido → Pedidos → Cliente
- Pedidos → Histórico do Pedido
- Produtos → Avaliações → Imagens das Avaliações
- Produtos → Imagens dos Produtos

### 17. Regras de Integridade
- Produtos não existem sem categoria.
- Variações pertencem obrigatoriamente a um produto.
- Avaliações vinculadas a um cliente e a um produto.
- Imagens pertencem obrigatoriamente ao seu registro principal.
- Itens do pedido armazenam o preço praticado no momento da compra.
- Histórico dos pedidos nunca removido automaticamente.
- Estoque controlado pelas variações dos produtos.
- Cliente só avalia produtos presentes em seus pedidos.

### 18. Índices Recomendados
SKU · Nome do produto · Categoria · Status do pedido · Código do cupom · Telefone do cliente · Data do pedido.

### 19. Diretrizes Obrigatórias para o Cloud Code
1. Implementar todas as tabelas previstas.
2. Usar chaves estrangeiras em todos os relacionamentos.
3. Garantir integridade referencial entre todas as entidades.
4. Evitar duplicação de informações.
5. Manter histórico permanente dos pedidos.
6. Controlar estoque pelas variações dos produtos.
7. Armazenar imagens em tabelas independentes.
8. Preservar o preço histórico dos itens do pedido.
9. Usar PostgreSQL como banco principal.
10. Criar o pedido antes do redirecionamento ao WhatsApp.

---

## Arquitetura 04 — Arquitetura das Regras de Negócio

**Status:** Aprovada

**Objetivo:** Definir todas as regras de funcionamento do sistema. *As regras aqui descritas têm prioridade sobre decisões de implementação. Nenhuma funcionalidade pode ser desenvolvida ignorando estas regras.*

### 2. Produtos
- **Cadastro obrigatório:** Nome, Descrição, Categoria, Preço, Cor, Tamanho, até 3 imagens, Quantidade em estoque, Status.
- **Status:** apenas Ativo ou Inativo. **Inativos não aparecem no catálogo.**
- **Estoque:** controle simples, cada combinação cor+tamanho tem sua própria quantidade (ex: Branca-P → 5; Branca-M → 8; Preta-G → 2).
- **Esgotado:** variação com qtd = 0 aparece como "Esgotada". Quando **todas** as variações esgotam → produto **removido automaticamente do catálogo público**.
- **Exclusão:** admin pode excluir; se o produto já foi usado em pedidos, a exclusão **não pode comprometer o histórico**.

### 3. Carrinho
- Funciona via sessão persistente: adicionar, remover, alterar quantidade, atualizar valores automaticamente.
- **Não permite quantidade superior ao estoque disponível.**
- Permanece salvo no mesmo dispositivo até concluir o envio; após pedido gerado + redirecionamento ao WhatsApp → **esvaziado automaticamente**.

### 4. Cliente
- Sem cadastro tradicional; dados informados só na finalização: Nome, Telefone, Endereço (quando necessário), Complemento, Bairro, Cidade, CEP.
- Após 1º preenchimento, dados ficam no mesmo dispositivo para agilizar futuras compras.

### 5. Pedido
- Criado automaticamente **antes** do redirecionamento ao WhatsApp.
- Registra: Cliente, Produtos, Quantidades, Variações, Valor total, Forma de entrega, Data.
- Depois, gera mensagem estruturada e abre o WhatsApp da loja.
- Se o cliente fechar o WhatsApp sem enviar, **nenhuma ação adicional**; o pedido permanece registrado.

### 6. Forma de Entrega
Apenas **Retirada na loja** e **Entrega local**. Sem transportadoras, sem Correios. Logística administrada pelo proprietário.

### 7. Administração dos Pedidos
- Todos os pedidos no painel admin. Admin visualiza: dados do cliente, produtos, quantidades, endereço, valor total, data.
- Pode alterar manualmente o status. **Status:** Pedido recebido · Em preparação · Saiu para entrega · Entregue · Cancelado.
- Toda alteração registrada no histórico.

### 8. Sessões
Sessão persistente mantém carrinho e dados pessoais preenchidos, enquanto os dados do navegador forem preservados no mesmo dispositivo.

### 9. Pesquisa
Localiza produtos por Nome, Categoria, Cor, Tamanho. Resultados com tempo de resposta reduzido.

### 10. Imagens
Até 3 por produto, exibidas na ordem definida pelo admin. Sistema impede envio acima do limite.

### 11. Painel Administrativo
Exclusivo do proprietário. Gerencia produtos, categorias, estoque, pedidos, clientes. **Todas as alterações refletem imediatamente na loja pública.**

### 12. Regras Gerais (obrigatórias)
- Não permitir estoque negativo.
- Não permitir adicionar ao carrinho acima do estoque disponível.
- Produtos inativos não exibidos.
- Produtos totalmente esgotados removidos automaticamente do catálogo.
- Cada variação com controle individual de estoque.
- Pedido criado antes da abertura do WhatsApp.
- Carrinho limpo automaticamente após redirecionamento ao WhatsApp.
- Histórico dos pedidos preservado permanentemente.
- Dados do cliente disponíveis no mesmo dispositivo para futuras compras.

### 13. Diretrizes Obrigatórias para o Cloud Code
1. Implementar todas as regras descritas.
2. **Centralizar as regras de negócio na camada de serviços do backend.**
3. Garantir que nenhuma regra crítica fique apenas no frontend.
4. Validar todas as operações também no servidor.
5. Preservar o histórico dos pedidos.
6. Controlar o estoque por variações de produto.
7. Sincronizar automaticamente o catálogo conforme o estoque disponível.
8. Gerar o pedido antes do redirecionamento ao WhatsApp.
9. Limpar automaticamente o carrinho após o redirecionamento ao WhatsApp.

---

## Arquitetura 05 — Arquitetura do Painel Administrativo

**Status:** Aprovada

**Objetivo:** Definir estrutura, organização e funcionamento do painel administrativo, responsável pelo gerenciamento completo da loja.

### 1. Objetivo
Ambiente exclusivo do proprietário. Prioriza simplicidade, rapidez e facilidade — tarefas diárias em poucos cliques. Otimizado para mobile, instalável como **PWA** (sem publicação na Play Store).

### 2. Acesso ao Painel
- Restrito ao administrador. Autenticação: **Usuário + Senha**.
- **NÃO haverá:** login com Google/Facebook, múltiplos administradores, controle de permissões, controle de cargos. Painel exclusivo do proprietário.

### 3. Dashboard
Exibe: total de pedidos, pedidos do dia, produtos cadastrados, produtos com baixo estoque, últimos pedidos recebidos. Só informações relevantes para gestão diária.

### 4. Gerenciamento de Produtos
Cadastrar, editar, excluir, ativar, inativar. Campos: Nome, Descrição, Categoria, Preço, Cor, Tamanho, Quantidade em estoque, até 3 imagens. **Alterações refletem imediatamente na loja pública.**

### 5. Gerenciamento de Categorias
Criar, editar, excluir. Usadas para organizar o catálogo.

### 6. Controle de Estoque
Por variação de produto — cada combinação com sua quantidade (ex: Branca P→10, M→5, G→2). Admin altera quantidades direto no painel. Variação com qtd = 0 → "Esgotada". Todas esgotadas → produto removido automaticamente do catálogo público.

### 7. Gerenciamento de Pedidos
Cada pedido exibe: número, nome do cliente, telefone, produtos, quantidade, valor total, forma de entrega, endereço completo (quando houver entrega), data, status atual.
**Status:** Pedido recebido · Em preparação · Saiu para entrega · Entregue · Cancelado. Alterações registradas no histórico.

### 8. Comunicação com o Cliente (ações rápidas por pedido)
Botões: **Abrir conversa no WhatsApp** · **Compartilhar pedido no WhatsApp** · **Copiar endereço completo** · **Copiar telefone do cliente**.

### 9. Cadastro de Clientes
Histórico com: Nome, Telefone, Endereço, Complemento, Bairro, Cidade, CEP, Total de pedidos, Data do último pedido. Opção de copiar endereço completo rapidamente.

### 10. Pesquisa
Pesquisa rápida para localizar Produtos, Categorias, Clientes, Pedidos — resultados em tempo reduzido.

### 11. Upload de Imagens
Máximo 3 por produto, ordenação, exclusão quando necessário, atualização imediata na loja pública.

### 12. Responsividade
Mobile First. Funciona em smartphones, tablets e computadores. Admin deve operar toda a loja só pelo celular.

### 13. Instalação como Aplicativo (PWA)
Instalação pelo navegador, ícone na tela inicial, acesso rápido, funcionamento tipo app. Sem publicação na Play Store.

### 14. Regras Gerais
- Apenas um administrador.
- Alterações refletem imediatamente na loja pública.
- Estoque por variações.
- Produtos inativos não aparecem para clientes.
- Produtos totalmente esgotados removidos automaticamente.
- Alterações de status registradas.
- Prioridade em rapidez e simplicidade.

### 15. Diretrizes Obrigatórias para o Cloud Code
1. Painel administrativo independente da loja pública.
2. Autenticação exclusiva para o administrador.
3. Mobile First em todas as telas.
4. Permitir instalação como PWA.
5. Pesquisa rápida em todos os módulos.
6. Atualizar automaticamente a loja pública após alterações administrativas.
7. Ações rápidas para atendimento via WhatsApp.
8. Cópia rápida de endereços e telefones.
9. Interface simples, objetiva e otimizada para uso diário.

---

## Arquitetura 06 — Arquitetura de Desenvolvimento e Padrões do Projeto

**Status:** Aprovada

**Objetivo:** Definir padrões técnicos, arquiteturais e de desenvolvimento para toda a implementação. *Nenhuma implementação pode contrariar as arquiteturas anteriores.*

### 2. Organização do Projeto
Único projeto Django — Monólito Modular. Cada módulo independente, responsabilidade única. Organização deve facilitar leitura, manutenção, evolução, reutilização interna, baixo acoplamento.

### 3. Estrutura dos Módulos
Cada módulo concentra apenas regras do seu domínio (Produtos, Categorias, Clientes, Pedidos, Carrinho, Painel Admin). Nenhum módulo contém regras de outro domínio.

### 4. Separação de Responsabilidades (camadas)
- **Models:** apenas representação dos dados; sem regras complexas de negócio.
- **Services:** **toda a lógica de negócio** vive aqui.
- **Views:** apenas recebem requisições, chamam serviços e retornam respostas; sem lógica de negócio.
- **Templates:** apenas apresentação.
- **JavaScript:** apenas melhora a experiência; **nenhuma regra crítica depende só do frontend.**

### 5. Regras de Desenvolvimento
Código simples, legível, baixo acoplamento, alta coesão, reutilização, evitar duplicação, evitar funções grandes, evitar dependências desnecessárias. **Priorizar soluções simples.**

### 6. Banco de Dados
Alterações via **migrations do Django**. Usar chaves estrangeiras, índices quando necessário, evitar redundância, preservar integridade referencial, relacionamentos claros. **Nunca alterar estrutura direto no banco em produção.**

### 7. Segurança
Toda entrada validada no backend: formulários, parâmetros, arquivos enviados, sanitização de entradas, proteção da autenticação do admin, **proteção CSRF do Django**. Nada vindo do frontend é confiável sem validação.

### 8. Performance
Evitar consultas repetitivas, usar consultas otimizadas, paginação em listas, carregar só o necessário, redimensionar imagens antes de armazenar quando necessário, evitar processamento desnecessário. Simplicidade antes de otimizações complexas.

### 9. Frontend
Mobile First. Layout responsivo, componentes reutilizáveis, navegação intuitiva, carregamento rápido, interface limpa, poucos cliques. Foco em facilidade de uso no mobile.

### 10. Padrões de Código
Nomes claros e descritivos, estrutura uniforme entre módulos, organização lógica dos arquivos, métodos pequenos e objetivos, separação clara de responsabilidades. Todo novo código segue o padrão existente.

### 11. Tratamento de Erros
Registrar erros no servidor, exibir mensagens compreensíveis, evitar interrupções inesperadas, preservar estabilidade. **Nenhum erro interno expõe informações sensíveis.**

### 12. Evolução do Projeto
Preparado para expansões — novas funcionalidades sem modificar significativamente módulos existentes. Preservar organização, clareza, compatibilidade, manutenibilidade.

### 13. Qualidade do Código
Legibilidade, simplicidade, consistência, organização, manutenibilidade, reutilização. Entre duas soluções, escolher a de **menor complexidade e maior facilidade de manutenção**.

### 14. Critérios de Aceitação
Funcionalidade concluída só quando: de acordo com todas as arquiteturas; não compromete funcionalidades existentes; respeita regras de negócio; funciona no mobile; possui validação no backend; integrada ao sistema; mantém organização arquitetural; não introduz duplicação desnecessária.

### 15. Diretrizes Obrigatórias para o Cloud Code
1. Respeitar todas as arquiteturas do projeto.
2. Django em Monólito Modular.
3. Centralizar regras de negócio na camada de serviços.
4. Evitar lógica de negócio em Views e Templates.
5. Código limpo, organizado e consistente.
6. Reutilizar componentes sempre que possível.
7. Manter baixo acoplamento entre módulos.
8. Priorizar simplicidade.
9. Validar todas as entradas no backend.
10. Interfaces Mobile First.
11. Toda nova funcionalidade segue os mesmos padrões.
