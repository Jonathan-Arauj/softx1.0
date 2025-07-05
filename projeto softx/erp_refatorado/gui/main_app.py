import tkinter
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

from erp_refatorado.database.database_manager import DatabaseManager
from erp_refatorado.business_logic.client_manager import ClientManager
from erp_refatorado.business_logic.user_manager import UserManager
from erp_refatorado.business_logic.supplier_manager import SupplierManager
from erp_refatorado.business_logic.product_manager import ProductManager
from erp_refatorado.models.models import Client, User, Supplier, Product
from erp_refatorado.gui.gui_components import GUIComponents

class Application:
    def __init__(self, master, logged_in_user=None):
        self.root = master
        self.logged_in_user = logged_in_user
        self.db_manager = DatabaseManager()
        self.client_manager = ClientManager()
        self.user_manager = UserManager()
        self.supplier_manager = SupplierManager()
        self.product_manager = ProductManager()
        self.current_frame = None
        self.frames = {}
        self.initialized_tabs = set()
        self.setup_gui()


    def setup_gui(self):
        self.root.title("SoftX ERP")
        self.root.geometry("1100x600")

        # Create a menu bar
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Início", command=lambda: self.show_frame("home"))
        file_menu.add_separator()  # Adiciona uma linha de separação
        file_menu.add_command(label="Sair", command=self.root.quit)

        # Cadastro Menu
        self.cadastro_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cadastro", menu=self.cadastro_menu)
        self.cadastro_menu.add_command(label="Usuário", command=lambda: self.show_frame("user_cadastro"))
        self.cadastro_menu.add_command(label="Cliente", command=lambda: self.show_frame("client_cadastro"))
        self.cadastro_menu.add_command(label="Fornecedor", command=lambda: self.show_frame("supplier_cadastro"))
        self.cadastro_menu.add_command(label="Produto", command=lambda: self.show_frame("product_cadastro"))

        # Consulta Menu
        self.consulta_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Consulta", menu=self.consulta_menu)
        self.consulta_menu.add_command(label="Usuário", command=lambda: self.show_frame("user_consulta"))
        self.consulta_menu.add_command(label="Cliente", command=lambda: self.show_frame("client_consulta"))
        self.consulta_menu.add_command(label="Fornecedor", command=lambda: self.show_frame("supplier_consulta"))
        self.consulta_menu.add_command(label="Produto", command=lambda: self.show_frame("product_consulta"))

        # Financeiro Menu
        self.financeiro_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Financeiro", menu=self.financeiro_menu)
        self.financeiro_menu.add_command(label="Contas a Pagar", command=lambda: GUIComponents.show_info("Financeiro", "Funcionalidade em desenvolvimento."))
        self.financeiro_menu.add_command(label="Contas a Receber", command=lambda: GUIComponents.show_info("Financeiro", "Funcionalidade em desenvolvimento."))

        # Vendas Menu
        self.vendas_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Vendas", menu=self.vendas_menu)
        self.vendas_menu.add_command(label="Nova Venda", command=lambda: self.show_frame("sale"))
        self.vendas_menu.add_command(label="Histórico de Vendas", command=lambda: GUIComponents.show_info("Vendas", "Funcionalidade em desenvolvimento."))

        # Initialize frames for each section
        # For simplicity, we'll use the same frame for cadastro and consulta for now, as the tabs already contain CRUD
        self.frames["home"] = Frame(self.root)
        self.frames["client_cadastro"] = Frame(self.root)
        self.frames["user_cadastro"] = Frame(self.root)
        self.frames["supplier_cadastro"] = Frame(self.root)
        self.frames["product_cadastro"] = Frame(self.root)
        self.frames["sale"] = Frame(self.root)

        # For consulta, we can reuse the same frames as they already have search/list functionality
        self.frames["client_consulta"] = self.frames["client_cadastro"]
        self.frames["user_consulta"] = self.frames["user_cadastro"]
        self.frames["supplier_consulta"] = self.frames["supplier_cadastro"]
        self.frames["product_consulta"] = self.frames["product_cadastro"]

        # Create content for each frame
        self.create_home_frame(self.frames["home"])  # Cria a tela de boas-vindas
        self.create_client_tab(self.frames["client_cadastro"])
        self.create_user_tab(self.frames["user_cadastro"])
        self.create_supplier_tab(self.frames["supplier_cadastro"])
        self.create_product_tab(self.frames["product_cadastro"])
        self.create_sale_tab(self.frames["sale"])

        # Show initial frame (e.g., client frame)
        self.show_frame("home")

    def create_home_frame(self, parent_frame):
        """Cria o conteúdo da tela inicial."""
        # Usamos um Label para mostrar o texto.
        # A fonte é grande e em negrito para dar destaque.
        welcome_label = Label(parent_frame, text="Bem-vindo ao SoftX ERP", font=("Arial", 24, "bold"), fg="#333")

        # .pack(expand=True) é um truque para centralizar o widget
        # tanto na horizontal quanto na vertical dentro do frame.
        welcome_label.pack(expand=True)


    def show_frame(self, frame_name):
        """Esconde o frame atual, mostra o frame solicitado e atualiza seus dados."""
        if self.current_frame:
            self.current_frame.pack_forget()

        frame = self.frames[frame_name]
        frame.pack(pady=10, expand=True, fill="both")
        self.current_frame = frame

        # Agora, apenas atualizamos os dados da aba que está sendo mostrada.
        # Isso é seguro porque sabemos que todos os widgets já foram criados na inicialização.
        print(f"Mostrando a aba: '{frame_name}'")
        if frame_name == "client_cadastro" or frame_name == "client_consulta":
            self.populate_client_list()
        elif frame_name == "user_cadastro" or frame_name == "user_consulta":
            self.populate_user_list()
        elif frame_name == "supplier_cadastro" or frame_name == "supplier_consulta":
            self.populate_supplier_list()
        elif frame_name == "product_cadastro" or frame_name == "product_consulta":
            self.populate_product_list()
            self.populate_supplier_combobox()
        elif frame_name == "sale":
            self.populate_client_combobox()
            self.populate_product_combobox()

    def create_client_tab(self, parent_frame):
        # --- Estilos com ttk (TEMA VERDE PROFISSIONAL) ---
        style = ttk.Style()
        style.theme_use("clam")
        COR_FUNDO = "#f5f5f5"
        COR_TEXTO = "#333333"
        COR_DESTAQUE = "#2e8b57"
        COR_DESTAQUE_CLARO = "#3cb371"
        parent_frame.configure(bg=COR_FUNDO)
        style.configure("TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=("Segoe UI", 10))
        style.configure("TButton", background=COR_DESTAQUE, foreground="white", font=("Segoe UI", 10, "bold"),
                        borderwidth=0, padding=5)
        style.map("TButton", background=[("active", COR_DESTAQUE_CLARO)])
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TFrame", background=COR_FUNDO)
        style.configure("TLabelframe", background=COR_FUNDO)
        style.configure("TLabelframe.Label", background=COR_FUNDO, foreground=COR_DESTAQUE,
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 10), fieldbackground=COR_FUNDO)
        style.map("Treeview", background=[("selected", COR_DESTAQUE)], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", background="#e0e0e0", font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", "#d0d0d0")])
        style.configure("Disabled.TEntry", fieldbackground="#eeeeee")

        # --- LAYOUT DA INTERFACE ---
        frame_formulario = ttk.LabelFrame(parent_frame, text="Dados do Cliente", padding="15")
        frame_formulario.pack(fill="x", padx=10, pady=10)
        frame_formulario.columnconfigure(1, weight=1)
        frame_formulario.columnconfigure(3, weight=1)

        # Coluna 1
        ttk.Label(frame_formulario, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.client_codigo_entry = ttk.Entry(frame_formulario, state="disabled", style="Disabled.TEntry")
        self.client_codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_formulario, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.client_nome_entry = ttk.Entry(frame_formulario)
        self.client_nome_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_formulario, text="CPF:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.client_cpf_entry = ttk.Entry(frame_formulario)
        self.client_cpf_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Data Nasc.:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.client_datanascimento_entry = DateEntry(frame_formulario, width=12, background=COR_DESTAQUE,
                                                     foreground="white", borderwidth=2, year=2000,
                                                     date_pattern='dd/mm/yyyy', font=("Segoe UI", 9))
        self.client_datanascimento_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_formulario, text="Bairro:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.client_bairro_entry = ttk.Entry(frame_formulario)
        self.client_bairro_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Coluna 2
        ttk.Label(frame_formulario, text="Email:").grid(row=0, column=2, padx=(15, 5), pady=5, sticky="w")
        self.client_email_entry = ttk.Entry(frame_formulario)
        self.client_email_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_formulario, text="Telefone:").grid(row=1, column=2, padx=(15, 5), pady=5, sticky="w")
        self.client_telefone_entry = ttk.Entry(frame_formulario)
        self.client_telefone_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_formulario, text="CEP:").grid(row=2, column=2, padx=(15, 5), pady=5, sticky="w")
        self.client_cep_entry = ttk.Entry(frame_formulario)
        self.client_cep_entry.grid(row=2, column=3, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_formulario, text="Rua:").grid(row=3, column=2, padx=(15, 5), pady=5, sticky="w")
        self.client_rua_entry = ttk.Entry(frame_formulario)
        self.client_rua_entry.grid(row=3, column=3, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_formulario, text="Cidade:").grid(row=4, column=2, padx=(15, 5), pady=5, sticky="w")
        self.client_cidade_entry = ttk.Entry(frame_formulario)
        self.client_cidade_entry.grid(row=4, column=3, padx=5, pady=5, sticky="ew")

        # ... (frames de botões, busca e tabela)
        frame_botoes_form = ttk.Frame(parent_frame)
        frame_botoes_form.pack(fill="x", padx=10, pady=5)
        ttk.Button(frame_botoes_form, text="Adicionar", command=self.add_client).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Alterar", command=self.update_client).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Deletar", command=self.delete_client).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Limpar", command=self.clear_client_entries).pack(side="left", padx=5)
        frame_lista = ttk.LabelFrame(parent_frame, text="Clientes Cadastrados", padding="10")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)
        frame_busca = ttk.Frame(frame_lista)
        frame_busca.pack(fill="x", pady=(0, 10))
        ttk.Label(frame_busca, text="Buscar Cliente:").pack(side="left", padx=(0, 5))
        self.client_search_entry = ttk.Entry(frame_busca)
        self.client_search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(frame_busca, text="Buscar", command=self.search_client).pack(side="left")
        frame_tabela = ttk.Frame(frame_lista)
        frame_tabela.pack(fill="both", expand=True)
        colunas = ("id", "nome", "cpf", "email", "telefone", "nascimento", "rua", "cep", "bairro", "cidade")
        self.client_list = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        scrollbar_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.client_list.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.client_list.xview)
        self.client_list.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.client_list.pack(side="left", fill="both", expand=True)
        self.client_list.heading("id", text="ID")
        self.client_list.heading("nome", text="Nome")
        self.client_list.heading("cpf", text="CPF")
        self.client_list.heading("email", text="Email")
        self.client_list.heading("telefone", text="Telefone")
        self.client_list.heading("nascimento", text="Nascimento")
        self.client_list.heading("rua", text="Rua")
        self.client_list.heading("cep", text="CEP")
        self.client_list.heading("bairro", text="Bairro")
        self.client_list.heading("cidade", text="Cidade")
        self.client_list.column("id", width=30, anchor="center")
        self.client_list.column("nome", width=150)
        self.client_list.column("cpf", width=100)
        self.client_list.column("email", width=150)
        self.client_list.column("telefone", width=100)
        self.client_list.column("nascimento", width=100, anchor="center")
        self.client_list.column("rua", width=150)
        self.client_list.column("cep", width=80, anchor="center")
        self.client_list.column("bairro", width=100)
        self.client_list.column("cidade", width=100)
        self.client_list.bind("<Double-1>", self.on_double_click_client)
        self.populate_client_list()

    def create_user_tab(self, parent_frame):
        # --- Estilos com ttk (TEMA VERDE PROFISSIONAL - Reutilizado da aba de cliente) ---
        # Nota: Idealmente, essa configuração de estilo deveria ser feita uma única vez no __init__ da classe principal,
        # para não ser repetida em cada aba. Mas para manter a função independente, vamos mantê-la aqui.
        style = ttk.Style()
        style.theme_use("clam")
        COR_FUNDO = "#f5f5f5"
        COR_TEXTO = "#333333"
        COR_DESTAQUE = "#2e8b57"
        COR_DESTAQUE_CLARO = "#3cb371"
        parent_frame.configure(bg=COR_FUNDO)
        style.configure("TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=("Segoe UI", 10))
        style.configure("TButton", background=COR_DESTAQUE, foreground="white", font=("Segoe UI", 10, "bold"),
                        borderwidth=0, padding=5)
        style.map("TButton", background=[("active", COR_DESTAQUE_CLARO)])
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TFrame", background=COR_FUNDO)
        style.configure("TLabelframe", background=COR_FUNDO)
        style.configure("TLabelframe.Label", background=COR_FUNDO, foreground=COR_DESTAQUE,
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 10), fieldbackground=COR_FUNDO)
        style.map("Treeview", background=[("selected", COR_DESTAQUE)], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", background="#e0e0e0", font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", "#d0d0d0")])
        style.configure("Disabled.TEntry", fieldbackground="#eeeeee")
        # Estilo para Combobox para se alinhar ao tema
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', COR_DESTAQUE)])
        style.map('TCombobox', selectforeground=[('readonly', 'white')])

        # --- LAYOUT DA INTERFACE ---
        frame_formulario = ttk.LabelFrame(parent_frame, text="Dados do Usuário", padding="15")
        frame_formulario.pack(fill="x", padx=10, pady=10)
        # Configura 4 colunas para o grid (label, entry, label, entry) e dá peso às colunas de entry
        frame_formulario.columnconfigure(1, weight=1)
        frame_formulario.columnconfigure(3, weight=1)

        # --- Formulário: Coluna 1 ---
        ttk.Label(frame_formulario, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.user_codigo_entry = ttk.Entry(frame_formulario, state="disabled", style="Disabled.TEntry")
        self.user_codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.user_nome_entry = ttk.Entry(frame_formulario)
        self.user_nome_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="CPF:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.user_cpf_entry = ttk.Entry(frame_formulario)
        self.user_cpf_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Data Nasc.:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.user_datanascimento_entry = DateEntry(frame_formulario, width=12, background=COR_DESTAQUE,
                                                   foreground="white", borderwidth=2, year=2000,
                                                   date_pattern='dd/mm/yyyy', font=("Segoe UI", 9))
        self.user_datanascimento_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_formulario, text="CEP:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.user_cep_entry = ttk.Entry(frame_formulario)
        self.user_cep_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Bairro:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.user_bairro_entry = ttk.Entry(frame_formulario)
        self.user_bairro_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Tipo de Usuário:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.user_tipo_combo = ttk.Combobox(frame_formulario, values=["admin", "vendedor", "financeiro", "estoque"],
                                            state="readonly")
        self.user_tipo_combo.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # --- Formulário: Coluna 2 ---
        ttk.Label(frame_formulario, text="Email:").grid(row=0, column=2, padx=(15, 5), pady=5, sticky="w")
        self.user_email_entry = ttk.Entry(frame_formulario)
        self.user_email_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Telefone:").grid(row=1, column=2, padx=(15, 5), pady=5, sticky="w")
        self.user_telefone_entry = ttk.Entry(frame_formulario)
        self.user_telefone_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Senha:").grid(row=2, column=2, padx=(15, 5), pady=5, sticky="w")
        self.user_senha_entry = ttk.Entry(frame_formulario, show="*")
        self.user_senha_entry.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        # Espaço vazio na linha 3 da coluna 2 para alinhar com o DateEntry

        ttk.Label(frame_formulario, text="Rua:").grid(row=4, column=2, padx=(15, 5), pady=5, sticky="w")
        self.user_rua_entry = ttk.Entry(frame_formulario)
        self.user_rua_entry.grid(row=4, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Cidade:").grid(row=5, column=2, padx=(15, 5), pady=5, sticky="w")
        self.user_cidade_entry = ttk.Entry(frame_formulario)
        self.user_cidade_entry.grid(row=5, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Permissão:").grid(row=6, column=2, padx=(15, 5), pady=5, sticky="w")
        self.user_permissao_combo = ttk.Combobox(frame_formulario, values=["padrao", "avancado"], state="readonly")
        self.user_permissao_combo.grid(row=6, column=3, padx=5, pady=5, sticky="ew")

        # --- Frame para os Botões ---
        frame_botoes_form = ttk.Frame(parent_frame)
        frame_botoes_form.pack(fill="x", padx=10, pady=5)
        ttk.Button(frame_botoes_form, text="Adicionar", command=self.add_user).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Alterar", command=self.update_user).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Deletar", command=self.delete_user).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Limpar", command=self.clear_user_entries).pack(side="left", padx=5)

        # --- Frame para a Lista de Usuários (Busca + Tabela) ---
        frame_lista = ttk.LabelFrame(parent_frame, text="Usuários Cadastrados", padding="10")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Busca ---
        frame_busca = ttk.Frame(frame_lista)
        frame_busca.pack(fill="x", pady=(0, 10))
        ttk.Label(frame_busca, text="Buscar Usuário:").pack(side="left", padx=(0, 5))
        self.user_search_entry = ttk.Entry(frame_busca)
        self.user_search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(frame_busca, text="Buscar", command=self.search_user).pack(side="left")

        # --- Tabela (Treeview) ---
        frame_tabela = ttk.Frame(frame_lista)
        frame_tabela.pack(fill="both", expand=True)

        # Defina as colunas que você realmente quer mostrar na lista. Menos é mais!
        colunas = ("id", "nome", "cpf", "email", "telefone", "tipo", "permissao")
        self.user_list = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.user_list.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.user_list.xview)
        self.user_list.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.user_list.pack(side="left", fill="both", expand=True)

        # Cabeçalhos
        self.user_list.heading("id", text="ID")
        self.user_list.heading("nome", text="Nome")
        self.user_list.heading("cpf", text="CPF")
        self.user_list.heading("email", text="Email")
        self.user_list.heading("telefone", text="Telefone")
        self.user_list.heading("tipo", text="Tipo")
        self.user_list.heading("permissao", text="Permissão")

        # Colunas
        self.user_list.column("id", width=40, anchor="center")
        self.user_list.column("nome", width=200)
        self.user_list.column("cpf", width=120)
        self.user_list.column("email", width=200)
        self.user_list.column("telefone", width=120)
        self.user_list.column("tipo", width=100, anchor="center")
        self.user_list.column("permissao", width=100, anchor="center")

        self.user_list.bind("<Double-1>", self.on_double_click_user)

        # Popula a lista com dados do banco de dados
        self.populate_user_list()

    def create_supplier_tab(self, parent_frame):
        # --- Estilos com ttk (TEMA VERDE PROFISSIONAL - Reutilizado das outras abas) ---
        style = ttk.Style()
        style.theme_use("clam")
        COR_FUNDO = "#f5f5f5"
        COR_TEXTO = "#333333"
        COR_DESTAQUE = "#2e8b57"
        COR_DESTAQUE_CLARO = "#3cb371"
        parent_frame.configure(bg=COR_FUNDO)
        style.configure("TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=("Segoe UI", 10))
        style.configure("TButton", background=COR_DESTAQUE, foreground="white", font=("Segoe UI", 10, "bold"),
                        borderwidth=0, padding=5)
        style.map("TButton", background=[("active", COR_DESTAQUE_CLARO)])
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TFrame", background=COR_FUNDO)
        style.configure("TLabelframe", background=COR_FUNDO)
        style.configure("TLabelframe.Label", background=COR_FUNDO, foreground=COR_DESTAQUE,
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 10), fieldbackground=COR_FUNDO)
        style.map("Treeview", background=[("selected", COR_DESTAQUE)], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", background="#e0e0e0", font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", "#d0d0d0")])
        style.configure("Disabled.TEntry", fieldbackground="#eeeeee")

        # --- LAYOUT DA INTERFACE ---
        frame_formulario = ttk.LabelFrame(parent_frame, text="Dados do Fornecedor", padding="15")
        frame_formulario.pack(fill="x", padx=10, pady=10)
        # Configura 4 colunas para o grid e dá peso às colunas de entry
        frame_formulario.columnconfigure(1, weight=1)
        frame_formulario.columnconfigure(3, weight=1)

        # --- Formulário: Coluna 1 ---
        ttk.Label(frame_formulario, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.supplier_codigo_entry = ttk.Entry(frame_formulario, state="disabled", style="Disabled.TEntry")
        self.supplier_codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Razão Social:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.supplier_razao_social_entry = ttk.Entry(frame_formulario)
        self.supplier_razao_social_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="CNPJ:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.supplier_cnpj_entry = ttk.Entry(frame_formulario)
        self.supplier_cnpj_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="CEP:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.supplier_cep_entry = ttk.Entry(frame_formulario)
        self.supplier_cep_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Bairro:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.supplier_bairro_entry = ttk.Entry(frame_formulario)
        self.supplier_bairro_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # --- Formulário: Coluna 2 ---

        ttk.Label(frame_formulario, text="Email:").grid(row=1, column=2, padx=(15, 5), pady=5, sticky="w")
        self.supplier_email_entry = ttk.Entry(frame_formulario)
        self.supplier_email_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Telefone:").grid(row=2, column=2, padx=(15, 5), pady=5, sticky="w")
        self.supplier_telefone_entry = ttk.Entry(frame_formulario)
        self.supplier_telefone_entry.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Rua:").grid(row=3, column=2, padx=(15, 5), pady=5, sticky="w")
        self.supplier_rua_entry = ttk.Entry(frame_formulario)
        self.supplier_rua_entry.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Cidade:").grid(row=4, column=2, padx=(15, 5), pady=5, sticky="w")
        self.supplier_cidade_entry = ttk.Entry(frame_formulario)
        self.supplier_cidade_entry.grid(row=4, column=3, padx=5, pady=5, sticky="ew")

        # --- Frame para os Botões ---
        frame_botoes_form = ttk.Frame(parent_frame)
        frame_botoes_form.pack(fill="x", padx=10, pady=5)
        ttk.Button(frame_botoes_form, text="Adicionar", command=self.add_supplier).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Alterar", command=self.update_supplier).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Deletar", command=self.delete_supplier).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Limpar", command=self.clear_supplier_entries).pack(side="left", padx=5)

        # --- Frame para a Lista de Fornecedores (Busca + Tabela) ---
        frame_lista = ttk.LabelFrame(parent_frame, text="Fornecedores Cadastrados", padding="10")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Busca ---
        frame_busca = ttk.Frame(frame_lista)
        frame_busca.pack(fill="x", pady=(0, 10))
        ttk.Label(frame_busca, text="Buscar Fornecedor:").pack(side="left", padx=(0, 5))
        self.supplier_search_entry = ttk.Entry(frame_busca)
        self.supplier_search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(frame_busca, text="Buscar", command=self.search_supplier).pack(side="left")

        # --- Tabela (Treeview) ---
        frame_tabela = ttk.Frame(frame_lista)
        frame_tabela.pack(fill="both", expand=True)

        # Defina as colunas mais importantes para a visualização inicial
        colunas = ("id", "razao_social", "cnpj", "email", "telefone")
        self.supplier_list = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.supplier_list.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.supplier_list.xview)
        self.supplier_list.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.supplier_list.pack(side="left", fill="both", expand=True)

        # Cabeçalhos
        self.supplier_list.heading("id", text="ID")
        self.supplier_list.heading("razao_social", text="Razão Social")
        self.supplier_list.heading("cnpj", text="CNPJ")
        self.supplier_list.heading("email", text="Email")
        self.supplier_list.heading("telefone", text="Telefone")

        # Colunas
        self.supplier_list.column("id", width=40, anchor="center")
        self.supplier_list.column("razao_social", width=200)
        self.supplier_list.column("cnpj", width=140)
        self.supplier_list.column("email", width=200)
        self.supplier_list.column("telefone", width=120)

        # Evento de duplo clique para carregar dados no formulário
        self.supplier_list.bind("<Double-1>", self.on_double_click_supplier)

        # Popula a lista com dados do banco de dados (função que você precisa ter)
        self.populate_supplier_list()

    def create_product_tab(self, parent_frame):
        # --- Estilos com ttk (TEMA VERDE PROFISSIONAL) ---
        style = ttk.Style()
        style.theme_use("clam")
        COR_FUNDO = "#f5f5f5"
        COR_TEXTO = "#333333"
        COR_DESTAQUE = "#2e8b57"
        COR_DESTAQUE_CLARO = "#3cb371"
        parent_frame.configure(bg=COR_FUNDO)
        style.configure("TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=("Segoe UI", 10))
        style.configure("TButton", background=COR_DESTAQUE, foreground="white", font=("Segoe UI", 10, "bold"),
                        borderwidth=0, padding=5)
        style.map("TButton", background=[("active", COR_DESTAQUE_CLARO)])
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TFrame", background=COR_FUNDO)
        style.configure("TLabelframe", background=COR_FUNDO)
        style.configure("TLabelframe.Label", background=COR_FUNDO, foreground=COR_DESTAQUE,
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 10), fieldbackground=COR_FUNDO)
        style.map("Treeview", background=[("selected", COR_DESTAQUE)], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", background="#e0e0e0", font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", "#d0d0d0")])
        style.configure("Disabled.TEntry", fieldbackground="#eeeeee")
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', COR_DESTAQUE)])
        style.map('TCombobox', selectforeground=[('readonly', 'white')])

        # --- LAYOUT DA INTERFACE ---
        # Usaremos um layout de duas colunas principais: uma para o formulário e outra para a lista
        main_frame = ttk.Frame(parent_frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.columnconfigure(1, weight=1)  # Coluna da lista de produtos terá mais peso

        # --- FRAME DO FORMULÁRIO (COLUNA 0) ---
        frame_formulario_container = ttk.Frame(main_frame)
        frame_formulario_container.grid(row=0, column=0, padx=(0, 10), sticky="ns")

        frame_formulario = ttk.LabelFrame(frame_formulario_container, text="Dados do Produto", padding="15")
        frame_formulario.pack(fill="x")

        # Widgets do formulário
        ttk.Label(frame_formulario, text="Código:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.product_codigo_entry = ttk.Entry(frame_formulario, state="disabled", style="Disabled.TEntry", width=10)
        self.product_codigo_entry.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        ttk.Label(frame_formulario, text="Nome:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.product_nome_entry = ttk.Entry(frame_formulario, width=30)
        self.product_nome_entry.grid(row=1, column=1, padx=5, pady=8, sticky="ew")

        ttk.Label(frame_formulario, text="Descrição:").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.product_descricao_entry = ttk.Entry(frame_formulario, width=30)
        self.product_descricao_entry.grid(row=2, column=1, padx=5, pady=8, sticky="ew")

        ttk.Label(frame_formulario, text="Preço (R$):").grid(row=3, column=0, padx=5, pady=8, sticky="w")
        self.product_preco_entry = ttk.Entry(frame_formulario, width=15)
        self.product_preco_entry.grid(row=3, column=1, padx=5, pady=8, sticky="w")

        ttk.Label(frame_formulario, text="Estoque:").grid(row=4, column=0, padx=5, pady=8, sticky="w")
        self.product_estoque_entry = ttk.Entry(frame_formulario, width=15)
        self.product_estoque_entry.grid(row=4, column=1, padx=5, pady=8, sticky="w")

        ttk.Label(frame_formulario, text="Fornecedor:").grid(row=5, column=0, padx=5, pady=8, sticky="w")
        self.product_fornecedor_combo = ttk.Combobox(frame_formulario, state="readonly", width=28)
        self.product_fornecedor_combo.grid(row=5, column=1, padx=5, pady=8, sticky="ew")

        # --- FRAME DE BOTÕES ---
        frame_botoes_form = ttk.Frame(frame_formulario_container)
        frame_botoes_form.pack(fill="x", pady=10)
        ttk.Button(frame_botoes_form, text="Adicionar", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Alterar", command=self.update_product).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Deletar", command=self.delete_product).pack(side="left", padx=5)
        ttk.Button(frame_botoes_form, text="Limpar", command=self.clear_product_entries).pack(side="left", padx=5)

        # --- FRAME DA LISTA (COLUNA 1) ---
        frame_lista = ttk.LabelFrame(main_frame, text="Produtos Cadastrados", padding="10")
        frame_lista.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        # --- Busca ---
        frame_busca = ttk.Frame(frame_lista)
        frame_busca.pack(fill="x", pady=(0, 10))
        ttk.Label(frame_busca, text="Buscar Produto:").pack(side="left", padx=(0, 5))
        self.product_search_entry = ttk.Entry(frame_busca)
        self.product_search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(frame_busca, text="Buscar", command=self.search_product).pack(side="left")

        # --- Tabela (Treeview) ---
        frame_tabela = ttk.Frame(frame_lista)
        frame_tabela.pack(fill="both", expand=True)

        colunas = ("id", "nome", "preco", "estoque", "fornecedor")  # Mostrando nome do fornecedor é mais útil
        self.product_list = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.product_list.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.product_list.xview)
        self.product_list.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.product_list.pack(side="left", fill="both", expand=True)

        # Cabeçalhos
        self.product_list.heading("id", text="ID")
        self.product_list.heading("nome", text="Nome do Produto")
        self.product_list.heading("preco", text="Preço (R$)")
        self.product_list.heading("estoque", text="Estoque")
        self.product_list.heading("fornecedor", text="Fornecedor")

        # Colunas
        self.product_list.column("id", width=50, anchor="center")
        self.product_list.column("nome", width=250)
        self.product_list.column("preco", width=100, anchor="e")  # 'e' = east (alinhado à direita)
        self.product_list.column("estoque", width=80, anchor="center")
        self.product_list.column("fornecedor", width=200)

        self.product_list.bind("<Double-1>", self.on_double_click_product)

        # Popula a lista e o combobox de fornecedores
        self.populate_product_list()
        # self.populate_supplier_combobox() # Você precisará criar esta função para carregar os fornecedores no ComboBox


    def create_sale_tab(self, parent_frame):
        """
        Cria a interface completa da aba de Vendas, com layout corrigido.
        """
        # --- Estilos (seu código de estilos permanece o mesmo) ---
        style = ttk.Style()
        style.theme_use("clam")
        COR_FUNDO = "#f5f5f5"
        COR_TEXTO = "#333333"
        COR_DESTAQUE = "#2e8b57"
        COR_DESTAQUE_CLARO = "#3cb371"
        parent_frame.configure(bg=COR_FUNDO)
        style.configure("TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=("Segoe UI", 10))
        style.configure("TButton", background=COR_DESTAQUE, foreground="white", font=("Segoe UI", 10, "bold"),
                        borderwidth=0, padding=5)
        style.map("TButton", background=[("active", COR_DESTAQUE_CLARO)])
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TFrame", background=COR_FUNDO)
        style.configure("TLabelframe", background=COR_FUNDO)
        style.configure("TLabelframe.Label", background=COR_FUNDO, foreground=COR_DESTAQUE,
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 10), fieldbackground=COR_FUNDO)
        style.map("Treeview", background=[("selected", COR_DESTAQUE)], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", background="#e0e0e0", font=("Segoe UI", 10, "bold"))
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', COR_DESTAQUE)])
        style.map('TCombobox', selectforeground=[('readonly', 'white')])
        style.configure("Total.TLabel", background=COR_FUNDO, foreground=COR_DESTAQUE, font=("Segoe UI", 16, "bold"))
        style.configure("Troco.TLabel", background=COR_FUNDO, foreground="#B22222", font=("Segoe UI", 14, "bold"))

        # --- FRAME PRINCIPAL ---
        main_frame = ttk.Frame(parent_frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- SEÇÃO 1: INFORMAÇÕES DA VENDA ---
        frame_venda_info = ttk.LabelFrame(main_frame, text="Dados da Venda", padding="10")
        # MUDANÇA DE LAYOUT AQUI
        frame_venda_info.pack(side="top", fill="x", pady=(0, 5))

        ttk.Label(frame_venda_info, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.sale_client_combo = ttk.Combobox(frame_venda_info, state="readonly", width=40)
        self.sale_client_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_venda_info, text="Data da Venda:").grid(row=0, column=2, padx=(20, 5), pady=5, sticky="w")
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        ttk.Label(frame_venda_info, text=data_hoje, font=("Segoe UI", 10, "bold")).grid(row=0, column=3, padx=5, pady=5,
                                                                                        sticky="w")

        # --- SEÇÃO 2: ADICIONAR PRODUTO ---
        frame_adicionar_item = ttk.LabelFrame(main_frame, text="Adicionar Produto", padding="10")
        # MUDANÇA DE LAYOUT AQUI
        frame_adicionar_item.pack(side="top", fill="x", pady=5)

        ttk.Label(frame_adicionar_item, text="Produto:").pack(side="left", padx=(0, 5))
        self.sale_product_combo = ttk.Combobox(frame_adicionar_item, state="readonly", width=40)
        self.sale_product_combo.pack(side="left", padx=5)
        ttk.Label(frame_adicionar_item, text="Qtd:").pack(side="left", padx=(15, 5))
        self.sale_quantidade_entry = ttk.Entry(frame_adicionar_item, width=8)
        self.sale_quantidade_entry.pack(side="left", padx=5)
        self.sale_quantidade_entry.insert(0, "1")
        ttk.Button(frame_adicionar_item, text="Adicionar Item", command=self.add_sale_item).pack(side="left",
                                                                                                 padx=(15, 5))

        # --- SEÇÃO 4: TOTAL E FINALIZAÇÃO (EMPACOTADA PRIMEIRO) ---
        frame_finalizacao = ttk.LabelFrame(main_frame, text="Finalização", padding="15")
        # MUDANÇA-CHAVE AQUI: Empacota no 'bottom' para reservar seu espaço
        frame_finalizacao.pack(side="bottom", fill="x", pady=(5, 0))

        frame_finalizacao.columnconfigure(1, weight=1)
        frame_finalizacao.columnconfigure(3, weight=1)
        frame_finalizacao.columnconfigure(4, weight=2)
        ttk.Label(frame_finalizacao, text="Subtotal (R$):").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.sale_subtotal_label = ttk.Label(frame_finalizacao, text="0.00", font=("Segoe UI", 10, "bold"))
        self.sale_subtotal_label.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        ttk.Label(frame_finalizacao, text="Desconto (R$):").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.sale_desconto_entry = ttk.Entry(frame_finalizacao, width=12)
        self.sale_desconto_entry.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        self.sale_desconto_entry.insert(0, "0.00")
        ttk.Label(frame_finalizacao, text="Valor Pago (R$):").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.sale_valor_pago_entry = ttk.Entry(frame_finalizacao, width=12)
        self.sale_valor_pago_entry.grid(row=2, column=1, padx=5, pady=3, sticky="w")
        self.sale_valor_pago_entry.insert(0, "0.00")
        ttk.Label(frame_finalizacao, text="VALOR TOTAL:").grid(row=0, column=2, padx=(20, 5), pady=3, sticky="w")
        self.sale_total_label = ttk.Label(frame_finalizacao, text="R$ 0.00", style="Total.TLabel")
        self.sale_total_label.grid(row=0, column=3, padx=5, pady=3, sticky="w")
        ttk.Label(frame_finalizacao, text="TROCO:").grid(row=1, column=2, padx=(20, 5), pady=3, sticky="w")
        self.sale_troco_label = ttk.Label(frame_finalizacao, text="R$ 0.00", style="Troco.TLabel")
        self.sale_troco_label.grid(row=1, column=3, padx=5, pady=3, sticky="w")
        frame_botoes_finais = ttk.Frame(frame_finalizacao)
        frame_botoes_finais.grid(row=0, column=4, rowspan=3, sticky="e", padx=(20, 0))
        ttk.Button(frame_botoes_finais, text="Cancelar Venda", command=self.clear_sale).pack(pady=4, fill='x',
                                                                                             expand=True)
        ttk.Button(frame_botoes_finais, text="Finalizar Venda", command=self.finalize_sale).pack(pady=4, fill='x',
                                                                                                 expand=True)
        self.sale_desconto_entry.bind("<KeyRelease>", self.update_sale_totals)
        self.sale_valor_pago_entry.bind("<KeyRelease>", self.update_sale_totals)

        # --- SEÇÃO 3: ITENS DA VENDA (EMPACOTADA POR ÚLTIMO) ---
        frame_itens_venda = ttk.LabelFrame(main_frame, text="Itens da Venda", padding="10")
        # MUDANÇA-CHAVE AQUI: Preenche o espaço restante
        frame_itens_venda.pack(side="top", fill="both", expand=True)

        colunas = ("produto_id", "produto_nome", "quantidade", "preco_unit", "subtotal")
        self.sale_items_list = ttk.Treeview(frame_itens_venda, columns=colunas, show="headings")
        scrollbar_y = ttk.Scrollbar(frame_itens_venda, orient="vertical", command=self.sale_items_list.yview)
        self.sale_items_list.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")
        self.sale_items_list.pack(side="left", fill="both", expand=True)
        self.sale_items_list.heading("produto_id", text="ID")
        self.sale_items_list.heading("produto_nome", text="Produto")
        self.sale_items_list.heading("quantidade", text="Qtd")
        self.sale_items_list.heading("preco_unit", text="Preço Unit. (R$)")
        self.sale_items_list.heading("subtotal", text="Subtotal (R$)")
        self.sale_items_list.column("produto_id", width=50, anchor="center")
        self.sale_items_list.column("produto_nome", width=300)
        self.sale_items_list.column("quantidade", width=80, anchor="center")
        self.sale_items_list.column("preco_unit", width=120, anchor="e")
        self.sale_items_list.column("subtotal", width=120, anchor="e")
    def populate_supplier_combobox(self):
        suppliers = self.supplier_manager.get_all_suppliers()
        supplier_names = [s.nome for s in suppliers]
        self.product_fornecedor_combo["values"] = supplier_names

    def populate_client_combobox(self):
        clients = self.client_manager.get_all_clients()
        client_names = [c.nome_cliente for c in clients]
        self.sale_client_combo["values"] = client_names

    def populate_product_combobox(self):
        products = self.product_manager.get_all_products()
        product_names = [p.nome_produto for p in products]
        self.sale_product_combo["values"] = product_names

    # --- Client Methods ---
    def add_client(self):
        try:
            nome = self.client_nome_entry.get()
            cpf = self.client_cpf_entry.get()
            email = self.client_email_entry.get()
            telefone = self.client_telefone_entry.get()
            nascimento_str = self.client_datanascimento_entry.get()
            rua = self.client_rua_entry.get()
            cep = self.client_cep_entry.get()
            bairro = self.client_bairro_entry.get()
            cidade = self.client_cidade_entry.get()

            if not all([nome, cpf, email, telefone, nascimento_str, rua, cep, bairro, cidade]):
                GUIComponents.show_error("Erro", "Todos os campos são obrigatórios.")
                return

            try:
                nascimento = datetime.strptime(nascimento_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                GUIComponents.show_error("Erro", "Formato de data de nascimento inválido. Use MM/DD/AA.")
                return

            client = Client(id_cliente=None, nome_cliente=nome, cpf_cliente=cpf, email_cliente=email, telefone_cliente=telefone, data_nascimento=nascimento, rua=rua, cep=cep, bairro=bairro, cidade=cidade)
            self.client_manager.add_client(client)
            GUIComponents.show_info("Sucesso", "Cliente adicionado com sucesso!")
            self.clear_client_entries()
            self.populate_client_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao adicionar cliente: {e}")

    def update_client(self):
        try:
            client_id = self.client_codigo_entry.get()
            if not client_id:
                GUIComponents.show_error("Erro", "Selecione um cliente para alterar.")
                return

            nome = self.client_nome_entry.get()
            cpf = self.client_cpf_entry.get()
            email = self.client_email_entry.get()
            telefone = self.client_telefone_entry.get()
            nascimento_str = self.client_datanascimento_entry.get()
            rua = self.client_rua_entry.get()
            cep = self.client_cep_entry.get()
            bairro = self.client_bairro_entry.get()
            cidade = self.client_cidade_entry.get()

            if not all([nome, cpf, email, telefone, nascimento_str, rua, cep, bairro, cidade]):
                GUIComponents.show_error("Erro", "Todos os campos são obrigatórios.")
                return

            try:
                nascimento = datetime.strptime(nascimento_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                GUIComponents.show_error("Erro", "Formato de data de nascimento inválido. Use DD/MM/AA.")
                return

            client = Client(id_cliente=int(client_id), nome_cliente=nome, cpf_cliente=cpf, email_cliente=email, telefone_cliente=telefone, data_nascimento=nascimento, rua=rua, cep=cep, bairro=bairro, cidade=cidade)
            self.client_manager.update_client(client)
            GUIComponents.show_info("Sucesso", "Cliente alterado com sucesso!")
            self.clear_client_entries()
            self.populate_client_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao alterar cliente: {e}")

    def delete_client(self):
        try:
            client_id = self.client_codigo_entry.get()
            if not client_id:
                GUIComponents.show_error("Erro", "Selecione um cliente para deletar.")
                return
            self.client_manager.delete_client(int(client_id))
            GUIComponents.show_info("Sucesso", "Cliente deletado com sucesso!")
            self.clear_client_entries()
            self.populate_client_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao deletar cliente: {e}")

    def search_client(self):
        try:
            search_term = self.client_search_entry.get()
            clients = self.client_manager.search_client(search_term)
            self.populate_client_list(clients)
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao buscar cliente: {e}")

    def clear_client_entries(self):
        self.client_codigo_entry.config(state="normal")
        self.client_codigo_entry.delete(0, END)
        self.client_codigo_entry.config(state="readonly")
        self.client_nome_entry.delete(0, END)
        self.client_cpf_entry.delete(0, END)
        self.client_email_entry.delete(0, END)
        self.client_telefone_entry.delete(0, END)
        self.client_datanascimento_entry.set_date(datetime.now())
        self.client_rua_entry.delete(0, END)
        self.client_cep_entry.delete(0, END)
        self.client_bairro_entry.delete(0, END)
        self.client_cidade_entry.delete(0, END)

    def populate_client_list(self, clients=None):
        for i in self.client_list.get_children():
            self.client_list.delete(i)
        if clients is None:
            clients = self.client_manager.get_all_clients()
        for client in clients:
            self.client_list.insert("", "end", values=(client.id_cliente, client.nome_cliente, client.cpf_cliente, client.email_cliente, client.telefone_cliente, client.data_nascimento, client.rua, client.cep, client.bairro, client.cidade))

    def on_double_click_client(self, event):
        selected_item = self.client_list.focus()
        if selected_item:
            values = self.client_list.item(selected_item, "values")
            self.clear_client_entries()
            self.client_codigo_entry.config(state="normal")
            self.client_codigo_entry.insert(0, values[0])
            self.client_codigo_entry.config(state="readonly")
            self.client_nome_entry.insert(0, values[1])
            self.client_cpf_entry.insert(0, values[2])
            self.client_email_entry.insert(0, values[3])
            self.client_telefone_entry.insert(0, values[4])
            # Assuming date format is YYYY-MM-DD from DB
            try:
                date_obj = datetime.strptime(values[5], "%Y-%m-%d")
                self.client_datanascimento_entry.set_date(date_obj)
            except ValueError:
                pass # Handle invalid date format if necessary
            self.client_rua_entry.insert(0, values[6])
            self.client_cep_entry.insert(0, values[7])
            self.client_bairro_entry.insert(0, values[8])
            self.client_cidade_entry.insert(0, values[9])

    # --- User Methods ---
    def add_user(self):
        try:
            nome = self.user_nome_entry.get()
            cpf = self.user_cpf_entry.get()
            email = self.user_email_entry.get()
            telefone = self.user_telefone_entry.get()
            nascimento_str = self.user_datanascimento_entry.get()
            rua = self.user_rua_entry.get()
            cep = self.user_cep_entry.get()
            bairro = self.user_bairro_entry.get()
            cidade = self.user_cidade_entry.get()
            senha = self.user_senha_entry.get()
            tipo = self.user_tipo_combo.get()
            permissao = self.user_permissao_combo.get()

            if not all([nome, cpf, email, telefone, nascimento_str, rua, cep, bairro, cidade, senha, tipo, permissao]):
                GUIComponents.show_error("Erro", "Todos os campos são obrigatórios.")
                return

            try:
                nascimento = datetime.strptime(nascimento_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                GUIComponents.show_error("Erro", "Formato de data de nascimento inválido. Use MM/DD/AA.")
                return

            user = User(id_usuario=None, nome_usuario=nome, cpf_usuario=cpf, email_usuario=email, telefone_usuario=telefone, data_nascimento=nascimento, rua=rua, cep=cep, bairro=bairro, cidade=cidade, senha=senha, tipo=tipo, permissao=permissao)
            self.user_manager.add_user(user)
            GUIComponents.show_info("Sucesso", "Usuário adicionado com sucesso!")
            self.clear_user_entries()
            self.populate_user_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao adicionar usuário: {e}")

    def update_user(self):
        try:
            user_id = self.user_codigo_entry.get()
            if not user_id:
                GUIComponents.show_error("Erro", "Selecione um usuário para alterar.")
                return

            nome = self.user_nome_entry.get()
            cpf = self.user_cpf_entry.get()
            email = self.user_email_entry.get()
            telefone = self.user_telefone_entry.get()
            nascimento_str = self.user_datanascimento_entry.get()
            rua = self.user_rua_entry.get()
            cep = self.user_cep_entry.get()
            bairro = self.user_bairro_entry.get()
            cidade = self.user_cidade_entry.get()
            tipo = self.user_tipo_combo.get()
            permissao = self.user_permissao_combo.get()

            # A senha é lida, mas não é obrigatória na validação
            senha = self.user_senha_entry.get()

            # --- VALIDAÇÃO CORRIGIDA ---
            # A senha FOI REMOVIDA da lista de campos obrigatórios
            campos_obrigatorios = [nome, cpf, email, tipo, permissao]  # Adapte se mais campos forem obrigatórios
            if not all(campos_obrigatorios):
                GUIComponents.show_error("Erro", "Os campos Nome, CPF, Email, Tipo e Permissão são obrigatórios.")
                return

            nascimento = None
            if nascimento_str:
                try:
                    nascimento = datetime.strptime(nascimento_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    GUIComponents.show_error("Erro", "Formato de data de nascimento inválido. Use DD/MM/AAAA.")
                    return

            user = User(id_usuario=int(user_id), nome_usuario=nome, cpf_usuario=cpf, email_usuario=email,
                        telefone_usuario=telefone, data_nascimento=nascimento, rua=rua, cep=cep,
                        bairro=bairro, cidade=cidade, senha=senha, tipo=tipo, permissao=permissao)

            # Chama o manager, que AGORA vamos corrigir
            self.user_manager.update_user(user)

            GUIComponents.show_info("Sucesso", "Usuário alterado com sucesso!")
            self.clear_user_entries()
            self.populate_user_list()

        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao alterar usuário: {e}")

    def delete_user(self):
        try:
            user_id = self.user_codigo_entry.get()
            if not user_id:
                GUIComponents.show_error("Erro", "Selecione um usuário para deletar.")
                return
            self.user_manager.delete_user(int(user_id))
            GUIComponents.show_info("Sucesso", "Usuário deletado com sucesso!")
            self.clear_user_entries()
            self.populate_user_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao deletar usuário: {e}")

    def search_user(self):
        try:
            search_term = self.user_nome_entry.get()
            users = self.user_manager.search_users(search_term)
            self.populate_user_list(users)
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao buscar usuário: {e}")

    def clear_user_entries(self):
        self.user_codigo_entry.config(state="normal")
        self.user_codigo_entry.delete(0, END)
        self.user_codigo_entry.config(state="readonly")
        self.user_nome_entry.delete(0, END)
        self.user_cpf_entry.delete(0, END)
        self.user_email_entry.delete(0, END)
        self.user_telefone_entry.delete(0, END)
        self.user_datanascimento_entry.set_date(datetime.now())
        self.user_rua_entry.delete(0, END)
        self.user_cep_entry.delete(0, END)
        self.user_bairro_entry.delete(0, END)
        self.user_cidade_entry.delete(0, END)
        self.user_senha_entry.delete(0, END)
        self.user_tipo_combo.set("")
        self.user_permissao_combo.set("")

    def populate_user_list(self, users=None):
        for i in self.user_list.get_children():
            self.user_list.delete(i)
        if users is None:
            users = self.user_manager.get_all_users()
        for user in users:
            self.user_list.insert("", "end", values=(user.id_usuario, user.nome_usuario, user.cpf_usuario, user.email_usuario, user.telefone_usuario, user.data_nascimento, user.rua, user.cep, user.bairro, user.cidade, user.tipo, user.permissao))

    def on_double_click_user(self, event):
        selected_item = self.user_list.focus()
        if selected_item:
            values = self.user_list.item(selected_item, "values")
            self.clear_user_entries()
            self.user_codigo_entry.config(state="normal")
            self.user_codigo_entry.insert(0, values[0])
            self.user_codigo_entry.config(state="readonly")
            self.user_nome_entry.insert(0, values[1])
            self.user_cpf_entry.insert(0, values[2])
            self.user_email_entry.insert(0, values[3])
            self.user_telefone_entry.insert(0, values[4])
            try:
                date_obj = datetime.strptime(values[5], "%Y-%m-%d")
                self.user_datanascimento_entry.set_date(date_obj)
            except ValueError:
                pass
            self.user_rua_entry.insert(0, values[6])
            self.user_cep_entry.insert(0, values[7])
            self.user_bairro_entry.insert(0, values[8])
            self.user_cidade_entry.insert(0, values[9])
            # Senha não é preenchida por segurança
            self.user_tipo_combo.set(values[10])
            self.user_permissao_combo.set(values[11])

    # --- Supplier Methods ---
    def add_supplier(self):
        try:
            razao_social = self.supplier_razao_social_entry.get()
            cnpj = self.supplier_cnpj_entry.get()
            email = self.supplier_email_entry.get()
            telefone = self.supplier_telefone_entry.get()
            rua = self.supplier_rua_entry.get()
            cep = self.supplier_cep_entry.get()
            bairro = self.supplier_bairro_entry.get()
            cidade = self.supplier_cidade_entry.get()

            if not all([ razao_social, cnpj, email, telefone, rua, cep, bairro, cidade]):
                GUIComponents.show_error("Erro", "Todos os campos são obrigatórios.")
                return

            supplier = Supplier(id_fornecedor=None, nome=razao_social, cnpj=cnpj, email=email, telefone=telefone, rua=rua, cep=cep, bairro=bairro, cidade=cidade)
            self.supplier_manager.add_supplier(supplier)
            GUIComponents.show_info("Sucesso", "Fornecedor adicionado com sucesso!")
            self.clear_supplier_entries()
            self.populate_supplier_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao adicionar fornecedor: {e}")

    def update_supplier(self):
        try:
            supplier_id = self.supplier_codigo_entry.get()
            if not supplier_id:
                GUIComponents.show_error("Erro", "Selecione um fornecedor para alterar.")
                return

            razao_social = self.supplier_razao_social_entry.get()
            cnpj = self.supplier_cnpj_entry.get()
            email = self.supplier_email_entry.get()
            telefone = self.supplier_telefone_entry.get()
            rua = self.supplier_rua_entry.get()
            cep = self.supplier_cep_entry.get()
            bairro = self.supplier_bairro_entry.get()
            cidade = self.supplier_cidade_entry.get()

            if not all([ razao_social, cnpj, email, telefone, rua, cep, bairro, cidade]):
                GUIComponents.show_error("Erro", "Todos os campos são obrigatórios.")
                return

            supplier = Supplier(id_fornecedor=int(supplier_id), nome=razao_social, cnpj=cnpj, email=email, telefone=telefone, rua=rua, cep=cep, bairro=bairro, cidade=cidade)
            self.supplier_manager.update_supplier(supplier)
            GUIComponents.show_info("Sucesso", "Fornecedor alterado com sucesso!")
            self.clear_supplier_entries()
            self.populate_supplier_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao alterar fornecedor: {e}")

    def delete_supplier(self):
        try:
            supplier_id = self.supplier_codigo_entry.get()
            if not supplier_id:
                GUIComponents.show_error("Erro", "Selecione um fornecedor para deletar.")
                return
            self.supplier_manager.delete_supplier(int(supplier_id))
            GUIComponents.show_info("Sucesso", "Fornecedor deletado com sucesso!")
            self.clear_supplier_entries()
            self.populate_supplier_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao deletar fornecedor: {e}")

    def search_supplier(self):
        try:
            search_term = self.supplier_nome_fantasia_entry.get()
            suppliers = self.supplier_manager.search_suppliers(search_term)
            self.populate_supplier_list(suppliers)
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao buscar fornecedor: {e}")

    def clear_supplier_entries(self):
        self.supplier_codigo_entry.config(state="normal")
        self.supplier_codigo_entry.delete(0, END)
        self.supplier_codigo_entry.config(state="readonly")
        self.supplier_razao_social_entry.delete(0, END)
        self.supplier_cnpj_entry.delete(0, END)
        self.supplier_email_entry.delete(0, END)
        self.supplier_telefone_entry.delete(0, END)
        self.supplier_rua_entry.delete(0, END)
        self.supplier_cep_entry.delete(0, END)
        self.supplier_bairro_entry.delete(0, END)
        self.supplier_cidade_entry.delete(0, END)

    def populate_supplier_list(self, suppliers=None):
        for i in self.supplier_list.get_children():
            self.supplier_list.delete(i)
        if suppliers is None:
            suppliers = self.supplier_manager.get_all_suppliers()
        for supplier in suppliers:
            self.supplier_list.insert("", "end", values=(supplier.id_fornecedor, supplier.nome, supplier.cnpj, supplier.email, supplier.telefone, supplier.rua, supplier.cep, supplier.bairro, supplier.cidade))

    def on_double_click_supplier(self, event):
        selected_item = self.supplier_list.focus()
        if selected_item:
            values = self.supplier_list.item(selected_item, "values")
            self.clear_supplier_entries()
            self.supplier_codigo_entry.config(state="normal")
            self.supplier_codigo_entry.insert(0, values[0])
            self.supplier_codigo_entry.config(state="readonly")
            self.supplier_razao_social_entry.insert(0, values[1])
            self.supplier_cnpj_entry.insert(0, values[2])
            self.supplier_email_entry.insert(0, values[3])
            self.supplier_telefone_entry.insert(0, values[4])
            self.supplier_rua_entry.insert(0, values[5])
            self.supplier_cep_entry.insert(0, values[6])
            self.supplier_bairro_entry.insert(0, values[7])
            self.supplier_cidade_entry.insert(0, values[8])

    # --- Product Methods ---
    def add_product(self):
        try:
            nome = self.product_nome_entry.get()
            descricao = self.product_descricao_entry.get()
            preco_str = self.product_preco_entry.get()
            estoque_str = self.product_estoque_entry.get()
            fornecedor_nome = self.product_fornecedor_combo.get()

            if not all([nome, descricao, preco_str, estoque_str, fornecedor_nome]):
                GUIComponents.show_error("Erro", "Todos os campos são obrigatórios.")
                return
            fornecedor_id = self.supplier_map.get(fornecedor_nome)

            if fornecedor_id is None:
                GUIComponents.show_error("Erro", f"Fornecedor '{fornecedor_nome}' não encontrado ou inválido.")
                return

            try:
                preco = float(preco_str)
                estoque = int(estoque_str)
            except ValueError:
                GUIComponents.show_error("Erro", "Preço e Estoque devem ser números válidos.")
                return

            fornecedor = self.supplier_manager.search_supplier(nome)
            if not fornecedor:
                GUIComponents.show_error("Erro", "Fornecedor não encontrado.")
                return
            fornecedor_id = fornecedor[0].id # Assuming unique name for simplicity

            product = Product(id_produto=None, nome=nome, descricao=descricao, preco=preco, estoque=estoque, fornecedor_id=fornecedor_id)
            self.product_manager.add_product(product)
            GUIComponents.show_info("Sucesso", "Produto adicionado com sucesso!")
            self.clear_product_entries()
            self.populate_product_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao adicionar produto: {e}")

    def update_product(self):
        try:
            product_id = self.product_codigo_entry.get()
            if not product_id:
                GUIComponents.show_error("Erro", "Selecione um produto para alterar.")
                return

            nome = self.product_nome_entry.get()
            descricao = self.product_descricao_entry.get()
            preco_str = self.product_preco_entry.get()
            estoque_str = self.product_estoque_entry.get()
            fornecedor_nome = self.product_fornecedor_combo.get()

            if not all([nome, descricao, preco_str, estoque_str, fornecedor_nome]):
                GUIComponents.show_error("Erro", "Todos os campos são obrigatórios.")
                return

            try:
                preco = float(preco_str)
                estoque = int(estoque_str)
            except ValueError:
                GUIComponents.show_error("Erro", "Preço e Estoque devem ser números válidos.")
                return

            fornecedor = self.supplier_manager.search_suppliers(fornecedor_nome)
            if not fornecedor:
                GUIComponents.show_error("Erro", "Fornecedor não encontrado.")
                return
            fornecedor_id = fornecedor[0].id

            product = Product(id=int(product_id), nome=nome, descricao=descricao, preco=preco, estoque=estoque, fornecedor_id=fornecedor_id)
            self.product_manager.update_product(product)
            GUIComponents.show_info("Sucesso", "Produto alterado com sucesso!")
            self.clear_product_entries()
            self.populate_product_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao alterar produto: {e}")

    def delete_product(self):
        try:
            product_id = self.product_codigo_entry.get()
            if not product_id:
                GUIComponents.show_error("Erro", "Selecione um produto para deletar.")
                return
            self.product_manager.delete_product(int(product_id))
            GUIComponents.show_info("Sucesso", "Produto deletado com sucesso!")
            self.clear_product_entries()
            self.populate_product_list()
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao deletar produto: {e}")

    def search_product(self):
        try:
            search_term = self.product_nome_entry.get()
            products = self.product_manager.search_products(search_term)
            self.populate_product_list(products)
        except Exception as e:
            GUIComponents.show_error("Erro", f"Erro ao buscar produto: {e}")

    def clear_product_entries(self):
        self.product_codigo_entry.config(state="normal")
        self.product_codigo_entry.delete(0, END)
        self.product_codigo_entry.config(state="readonly")
        self.product_nome_entry.delete(0, END)
        self.product_descricao_entry.delete(0, END)
        self.product_preco_entry.delete(0, END)
        self.product_estoque_entry.delete(0, END)
        self.product_fornecedor_combo.set("")

    def populate_product_list(self, products=None):
        for i in self.product_list.get_children():
            self.product_list.delete(i)
        if products is None:
            products = self.product_manager.get_all_products()
        for product in products:
            # Get supplier name for display
            supplier_name = ""
            if product.fornecedor_id:
                supplier = self.supplier_manager.get_supplier_by_id(product.fornecedor_id)
                if supplier:
                    supplier_name = supplier.nome_fantasia
            self.product_list.insert("", "end", values=(product.id, product.nome, product.descricao, product.preco, product.estoque, supplier_name))

    def on_double_click_product(self, event):
        selected_item = self.product_list.focus()
        if selected_item:
            values = self.product_list.item(selected_item, "values")
            self.clear_product_entries()
            self.product_codigo_entry.config(state="normal")
            self.product_codigo_entry.insert(0, values[0])
            self.product_codigo_entry.config(state="readonly")
            self.product_nome_entry.insert(0, values[1])
            self.product_descricao_entry.insert(0, values[2])
            self.product_preco_entry.insert(0, values[3])
            self.product_estoque_entry.insert(0, values[4])
            self.product_fornecedor_combo.set(values[5])

    # --- Sale Methods ---
    def add_sale_item(self):
        # Implement logic to add item to a temporary list for the current sale
        GUIComponents.show_info("Venda", "Funcionalidade de adicionar item em desenvolvimento.")

    def finalize_sale(self):
        # Implement logic to finalize the sale, update stock, record transaction
        GUIComponents.show_info("Venda", "Funcionalidade de finalizar venda em desenvolvimento.")

    # Em gui/main_app.py, dentro da classe Application

    def update_sale_totals(self, event=None):
        """
        Recalcula o subtotal, o total geral e o troco.
        É chamado sempre que um item é adicionado/removido ou quando
        os valores de desconto/pago são alterados.
        """
        try:
            # 1. Calcular o Subtotal a partir da Treeview
            subtotal = 0.0
            for item_id in self.sale_items_list.get_children():
                # A coluna 'subtotal' é a 5ª (índice 4)
                valor_item_str = self.sale_items_list.item(item_id, "values")[4]
                subtotal += float(valor_item_str)

            self.sale_subtotal_label.config(text=f"{subtotal:.2f}")

            # 2. Obter Desconto e Valor Pago
            desconto_str = self.sale_desconto_entry.get().replace(",", ".") or "0"
            valor_pago_str = self.sale_valor_pago_entry.get().replace(",", ".") or "0"

            desconto = float(desconto_str)
            valor_pago = float(valor_pago_str)

            # 3. Calcular Total e Troco
            total_final = subtotal - desconto
            troco = valor_pago - total_final if valor_pago > 0 else 0.0

            # Garante que total e troco não sejam negativos
            total_final = max(0, total_final)
            troco = max(0, troco)

            # 4. Atualizar os Labels
            self.sale_total_label.config(text=f"R$ {total_final:.2f}")
            self.sale_troco_label.config(text=f"R$ {troco:.2f}")

        except (ValueError, IndexError):
            # Se houver um erro de conversão (ex: texto no campo de preço)
            self.sale_total_label.config(text="R$ ---")
            self.sale_troco_label.config(text="R$ ---")

    def clear_sale(self):
        """
        Limpa todos os campos da aba de vendas para iniciar uma nova venda.
        """
        # ... (código anterior para limpar a Treeview e os comboboxes) ...
        for item in self.sale_items_list.get_children():
            self.sale_items_list.delete(item)
        self.sale_client_combo.set('')
        self.sale_product_combo.set('')
        self.sale_quantidade_entry.delete(0, 'end')
        self.sale_quantidade_entry.insert(0, "1")

        # ATUALIZAÇÃO: Limpar os novos campos financeiros
        self.sale_desconto_entry.delete(0, 'end')
        self.sale_desconto_entry.insert(0, "0.00")
        self.sale_valor_pago_entry.delete(0, 'end')
        self.sale_valor_pago_entry.insert(0, "0.00")

        # Chama a função de update para zerar os labels
        self.update_sale_totals()
        print("Tela de vendas limpa.")

    # Não se esqueça de chamar self.update_sale_totals() também
    # no final da sua função 'add_sale_item' e da função que remove um item (se tiver uma).

if __name__ == "__main__":
    # This block will not be executed when run via `python -m erp_refatorado.main`
    # as main.py is the entry point now.
    root = tkinter.Tk()
    app = Application(root)
    root.mainloop()


