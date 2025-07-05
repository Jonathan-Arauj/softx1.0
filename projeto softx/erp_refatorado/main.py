# Em main.py

import tkinter as tk
from gui.login_app import LoginApp  # Importa a classe da tela de login
from gui.main_app import Application  # Importa a classe da aplicação principal
from database.database_manager import DatabaseManager  # Importa para criar as tabelas


def main():
    """
    Função principal que gerencia o fluxo de login e a inicialização da aplicação.
    """
    # Passo 1: Garantir que o banco de dados e as tabelas existam
    # Isso é importante para que o login possa consultar a tabela de usuários
    print("Inicializando o sistema e verificando o banco de dados...")
    db_manager = DatabaseManager()
    # A classe DatabaseManager já deve ter o método para criar as tabelas
    if hasattr(db_manager, 'create_tables'):
        db_manager.create_tables()
    else:
        # Se não tiver, você pode adicionar a lógica aqui ou na própria classe
        print("Aviso: Método 'create_tables' não encontrado no DatabaseManager.")
        print("Certifique-se de que as tabelas já existem no banco de dados.")

    # Passo 2: Iniciar a tela de login
    login_root = tk.Tk()
    login_app = LoginApp(login_root)
    login_root.mainloop()  # Este loop pausa o código aqui até a janela de login ser fechada

    # Passo 3: Verificar se o login foi bem-sucedido
    # O código só continuará a partir daqui depois que login_root.mainloop() terminar
    if login_app.logged_in_user:
        print(
            f"Login bem-sucedido! Iniciando aplicação principal para o usuário: {login_app.logged_in_user.nome_usuario}")

        # Passo 4: Iniciar a aplicação principal
        main_root = tk.Tk()
        app = Application(main_root, logged_in_user=login_app.logged_in_user)  # Passa o usuário logado para a app
        main_root.mainloop()
    else:
        print("Login cancelado ou falhou. Encerrando o programa.")


if __name__ == "__main__":
    main()