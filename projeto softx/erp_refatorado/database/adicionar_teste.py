# Em adicionar_dados_teste.py

import sqlite3
import bcrypt
import random
from faker import Faker

# Importa o caminho do banco de dados do nosso arquivo de configuração central
from config import DB_PATH


def add_test_data(db_path, num_clients, num_users):
    """
    Conecta ao banco de dados e insere uma quantidade definida de clientes e usuários.
    Assume que as tabelas já existem.
    """
    # Inicializa o Faker para gerar dados em português do Brasil
    fake = Faker('pt_BR')

    conexao = None
    try:
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()
        print(f"Conexão com o banco de dados em '{db_path}' estabelecida.")

        # --- INSERÇÃO DE DADOS ---
        print("\nIniciando inserção de dados...")

        # Inserindo Clientes
        print(f"Gerando e inserindo {num_clients} clientes...")
        clientes_adicionados = 0
        for _ in range(num_clients):
            try:
                cliente = (
                    fake.name(),
                    fake.cpf(),
                    fake.unique.email(),
                    fake.phone_number(),
                    fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
                    fake.street_name(),
                    fake.postcode(),
                    fake.bairro(),
                    fake.city()
                )
                cursor.execute(
                    "INSERT INTO clientes (nome_cliente, cpf_cliente, email_cliente, telefone_cliente, data_nascimento, rua, cep, bairro, cidade) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    cliente)
                clientes_adicionados += 1
            except sqlite3.IntegrityError:
                continue  # Pula se gerar um CPF/email duplicado
        print(f"-> {clientes_adicionados} clientes processados.")

        # Inserindo Usuários
        print(f"\nGerando e inserindo {num_users} usuários...")
        tipos_usuario = ['vendedor', 'financeiro', 'estoque']
        usuarios_adicionados = 0

        # Garante que o usuário admin exista
        try:
            admin_senha = bcrypt.hashpw(b"admin", bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO usuarios (nome_usuario, cpf_usuario, email_usuario, telefone_usuario, data_nascimento, rua, cep, bairro, cidade, senha, tipo, permissao) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                ('Admin Principal', '999.999.999-99', 'admin@sistema.com', fake.phone_number(),
                 fake.date_of_birth(minimum_age=25, maximum_age=60).strftime('%Y-%m-%d'), fake.street_name(),
                 fake.postcode(), fake.bairro(), fake.city(), admin_senha, 'admin', 'avancado'))
            usuarios_adicionados += 1
        except sqlite3.IntegrityError:
            print("-> Aviso: Usuário admin (admin@sistema.com) já existe.")

        # Gera o restante dos usuários
        for _ in range(num_users - usuarios_adicionados):
            try:
                senha_padrao = bcrypt.hashpw(b"123456", bcrypt.gensalt())
                usuario = (
                    fake.name(),
                    fake.cpf(),
                    fake.unique.email(),
                    fake.phone_number(),
                    fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d'),
                    fake.street_name(),
                    fake.postcode(),
                    fake.bairro(),
                    fake.city(),
                    senha_padrao,
                    random.choice(tipos_usuario),
                    'padrao'
                )
                cursor.execute(
                    "INSERT INTO usuarios (nome_usuario, cpf_usuario, email_usuario, telefone_usuario, data_nascimento, rua, cep, bairro, cidade, senha, tipo, permissao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    usuario)
                usuarios_adicionados += 1
            except sqlite3.IntegrityError:
                continue
        print(f"-> {usuarios_adicionados} usuários processados no total.")

        conexao.commit()
        print("\nCommit realizado. Dados salvos com sucesso.")

    except sqlite3.OperationalError as e:
        print(f"\nERRO: {e}")
        print("Verifique se as tabelas 'clientes' e 'usuarios' realmente existem no banco de dados.")
    finally:
        if conexao:
            conexao.close()
            print("Conexão com o banco de dados fechada.")


if __name__ == "__main__":
    print("--- SCRIPT PARA POPULAR BANCO DE DADOS ---")

    # === CONFIGURE AQUI A QUANTIDADE ===
    quantidade_clientes = 50
    quantidade_usuarios = 10

    add_test_data(DB_PATH, quantidade_clientes, quantidade_usuarios)
    print("\n--- PROCESSO CONCLUÍDO ---")