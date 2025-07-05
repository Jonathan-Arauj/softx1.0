import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import json
from PIL import Image, ImageTk  # Importa o Pillow

# Adapte os imports para a sua estrutura de projeto
from erp_refatorado.business_logic.user_manager import UserManager
from erp_refatorado.models.models import User


class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Login - SoftX ERP")

        # --- Configuração da Janela ---
        window_width = 350
        window_height = 400
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        master.resizable(False, False)

        self.logged_in_user = None
        self.user_manager = UserManager()

        # --- Estilos ---
        style = ttk.Style(master)
        style.theme_use("clam")
        COR_FUNDO = "#ffffff"
        COR_FUNDO_FRAME = "#f5f5f5"
        COR_DESTAQUE = "#2e8b57"
        COR_DESTAQUE_CLARO = "#3cb371"
        master.configure(bg=COR_FUNDO)

        style.configure("TLabel", background=COR_FUNDO_FRAME, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=COR_FUNDO, font=("Segoe UI", 20, "bold"), foreground=COR_DESTAQUE)
        style.configure("TButton", background=COR_DESTAQUE, foreground="white", font=("Segoe UI", 11, "bold"),
                        padding=8, borderwidth=0)
        style.map("TButton", background=[("active", COR_DESTAQUE_CLARO)])
        style.configure("TEntry", font=("Segoe UI", 11), padding=5)
        style.configure("TCheckbutton", background=COR_FUNDO_FRAME, font=("Segoe UI", 9))
        style.configure("Login.TFrame", background=COR_FUNDO_FRAME, relief="solid", borderwidth=1)

        # --- Carregar Ícones ---
        try:
            # Coloque os ícones em uma pasta 'assets' ou mude o caminho
            user_img_path = "assets/user_icon.png"
            pass_img_path = "assets/pass_icon.png"
            self.user_icon = ImageTk.PhotoImage(Image.open(user_img_path).resize((16, 16)))
            self.pass_icon = ImageTk.PhotoImage(Image.open(pass_img_path).resize((16, 16)))
        except FileNotFoundError:
            self.user_icon = None
            self.pass_icon = None
            print("Aviso: Arquivos de ícone não encontrados. A tela de login funcionará sem eles.")

        # --- Layout ---
        # Título
        ttk.Label(master, text="SoftX ERP", style="Header.TLabel", background=COR_FUNDO).pack(pady=(30, 10))

        # Frame principal para o formulário
        main_frame = ttk.Frame(master, style="Login.TFrame", padding=(20, 20))
        main_frame.pack(expand=True, padx=20, pady=10, fill="x")
        main_frame.columnconfigure(1, weight=1)

        # Ícone e Campo de Usuário
        if self.user_icon:
            ttk.Label(main_frame, image=self.user_icon, background=COR_FUNDO_FRAME).grid(row=0, column=0, sticky='w',
                                                                                         padx=(0, 5))
        self.username_entry = ttk.Entry(main_frame, font=("Segoe UI", 11))
        self.username_entry.grid(row=0, column=1, sticky='ew', pady=5)
        self.username_entry.insert(0, "Usuário")  # Placeholder text

        # Ícone e Campo de Senha
        if self.pass_icon:
            ttk.Label(main_frame, image=self.pass_icon, background=COR_FUNDO_FRAME).grid(row=1, column=0, sticky='w',
                                                                                         padx=(0, 5))
        self.password_entry = ttk.Entry(main_frame, font=("Segoe UI", 11), show="*")
        self.password_entry.grid(row=1, column=1, sticky='ew', pady=5)
        self.password_entry.insert(0, "Senha")  # Placeholder text

        # Placeholders (texto cinza que some ao clicar)
        self.setup_placeholder(self.username_entry, "Usuário")
        self.setup_placeholder(self.password_entry, "Senha")

        # Opções Adicionais
        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(main_frame, text="Ver Senha", variable=self.show_password_var,
                                                   command=self.toggle_password_visibility)
        self.show_password_check.grid(row=2, column=1, sticky='w', pady=(5, 0))

        self.remember_user_var = tk.BooleanVar()
        self.remember_user_check = ttk.Checkbutton(main_frame, text="Lembrar Usuário", variable=self.remember_user_var)
        self.remember_user_check.grid(row=2, column=1, sticky='e', pady=(5, 0))

        # Botão de Login
        self.login_button = ttk.Button(main_frame, text="ENTRAR", command=self.login, style="TButton")
        self.login_button.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(20, 10))

        self.master.bind('<Return>', self.login)
        self.load_remembered_user()

    # --- Funções para Placeholders ---
    def setup_placeholder(self, entry, text):
        entry.placeholder = text
        entry.placeholder_color = 'grey'
        entry.default_fg_color = entry['foreground']

        def on_focusin(event):
            if entry.get() == entry.placeholder:
                entry.delete(0, 'end')
                entry.config(foreground=entry.default_fg_color, show="*" if entry.placeholder == "Senha" else "")

        def on_focusout(event):
            if not entry.get():
                entry.insert(0, entry.placeholder)
                entry.config(foreground=entry.placeholder_color, show="" if entry.placeholder == "Senha" else "*")

        entry.bind("<FocusIn>", on_focusin)
        entry.bind("<FocusOut>", on_focusout)

        on_focusout(None)  # Inicializa o placeholder

    # --- Outras funções (login, remember_user, etc.) ---
    # As funções abaixo são as mesmas da versão anterior. Você pode copiá-las.

    def toggle_password_visibility(self):
        # A lógica para o placeholder de senha é um pouco diferente
        if self.password_entry.get() != self.password_entry.placeholder:
            if self.show_password_var.get():
                self.password_entry.config(show="")
            else:
                self.password_entry.config(show="*")

    def remember_user(self, username):
        config_data = {'last_user': username}
        try:
            with open('login_config.json', 'w') as f:
                json.dump(config_data, f)
        except Exception as e:
            print(f"Não foi possível salvar o usuário: {e}")

    def load_remembered_user(self):
        if os.path.exists('login_config.json'):
            try:
                with open('login_config.json', 'r') as f:
                    config_data = json.load(f)
                    last_user = config_data.get('last_user')
                    if last_user:
                        self.username_entry.delete(0, 'end')
                        self.username_entry.insert(0, last_user)
                        self.username_entry.config(foreground=self.username_entry.default_fg_color)
                        self.remember_user_var.set(True)
                        self.password_entry.focus_set()
            except Exception as e:
                print(f"Não foi possível carregar o usuário salvo: {e}")

    def forget_user(self):
        if os.path.exists('login_config.json'): os.remove('login_config.json')

    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == self.username_entry.placeholder or password == self.password_entry.placeholder:
            messagebox.showwarning("Atenção", "Por favor, preencha o usuário e a senha.")
            return

        authenticated_user = self.user_manager.authenticate_user(username, password)
        if authenticated_user:
            self.logged_in_user = authenticated_user
            if self.remember_user_var.get():
                self.remember_user(username)
            else:
                self.forget_user()
            self.master.destroy()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")
            # Não limpa a senha aqui, para não interferir com o placeholder