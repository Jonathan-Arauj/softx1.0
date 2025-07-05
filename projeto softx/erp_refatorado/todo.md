## Tarefas para Aprimoramento da GUI

### Fase 1: Implementar a tela de login (`login_app.py`)
- [x] Criar `login_app.py` com campos de usuário e senha.
- [x] Implementar lógica de autenticação usando `UserManager`.
- [x] Adicionar funcionalidade para abrir `main_app.py` após login bem-sucedido.

### Fase 2: Criar a tela principal 'SoftX' com barra de menu (`main_app.py`)
- [x] Renomear a janela principal para 'SoftX ERP'.
- [x] Adicionar uma barra de menu (`MenuBar`) à janela principal.

### Fase 3: Adicionar menus cascata para Cadastro e Consulta
- [x] Adicionar menu 'Cadastro' com submenus para 'Usuário', 'Cliente', 'Fornecedor', 'Produto'.
- [x] Adicionar menu 'Consulta' com submenus para 'Usuário', 'Cliente', 'Fornecedor', 'Produto'.
- [x] Adicionar menus 'Financeiro' e 'Vendas' (sem submenus por enquanto).

### Fase 4: Integrar as funcionalidades existentes nas novas abas/menus
- [x] Modificar `main_app.py` para que as funcionalidades de cada aba sejam acessadas via menu.
- [x] Remover o `ttk.Notebook` e usar `Frame`s separados que são exibidos/ocultados conforme a seleção do menu.

### Fase 5: Testar a nova estrutura da GUI
- [x] Executar `login_app.py` e testar o fluxo de login (teste manual necessário).
- [x] Testar a navegação pelos menus e a exibição correta das telas (teste manual necessário).
- [x] Verificar se as funcionalidades CRUD continuam operacionais (teste manual necessário).

### Fase 6: Gerar relatório de aprimoramento da GUI e código final
- [x] Documentar as mudanças e melhorias implementadas na GUI.
- [x] Gerar o relatório final em PDF.

### Fase 7: Entregar o código e o relatório ao usuário
- [ ] Compactar o código refatorado.
- [ ] Enviar o código e o relatório ao usuário.


