import sqlite3
from config import DB_PATH

class DatabaseManager:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        with self as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios(
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_usuario TEXT NOT NULL,
                    cpf_usuario TEXT NOT NULL UNIQUE,
                    email_usuario TEXT NOT NULL UNIQUE,
                    telefone_usuario TEXT NOT NULL,
                    data_nascimento TEXT NOT NULL,
                    rua TEXT NOT NULL,
                    cep TEXT NOT NULL,
                    bairro TEXT NOT NULL,
                    cidade TEXT NOT NULL,
                    senha TEXT NOT NULL,
                    tipo TEXT NOT NULL CHECK(tipo IN (\'admin\', \'vendedor\', \'financeiro\', \'estoque\')),
                    permissao TEXT NOT NULL DEFAULT \'padrao\'
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_cliente TEXT NOT NULL,
                    cpf_cliente TEXT NOT NULL UNIQUE,
                    email_cliente TEXT NOT NULL UNIQUE,
                    telefone_cliente TEXT NOT NULL,
                    data_nascimento TEXT NOT NULL,
                    rua TEXT NOT NULL,
                    cep TEXT NOT NULL,
                    bairro TEXT NOT NULL,
                    cidade TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fornecedores (
                    id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cnpj TEXT NOT NULL UNIQUE,
                    telefone TEXT,
                    email TEXT UNIQUE,
                    rua TEXT NOT NULL,
                    cep TEXT NOT NULL,
                    bairro TEXT NOT NULL,
                    cidade TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    preco_venda REAL NOT NULL,
                    preco_compra REAL NOT NULL,
                    fornecedor_id INTEGER,
                    FOREIGN KEY(fornecedor_id) REFERENCES fornecedores(id_fornecedor)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estoque (
                    id_estoque INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER NOT NULL,
                    quantidade INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY(produto_id) REFERENCES produtos(id_produto)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendas (
                    id_vendas INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    usuario_id INTEGER NOT NULL,
                    data_venda TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    total REAL NOT NULL,
                    FOREIGN KEY(cliente_id) REFERENCES clientes(id_cliente),
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id_usuario)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compras (
                    id_compras INTEGER PRIMARY KEY AUTOINCREMENT,
                    fornecedor_id INTEGER NOT NULL,
                    usuario_id INTEGER NOT NULL,
                    data_compra TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    total REAL NOT NULL,
                    FOREIGN KEY(fornecedor_id) REFERENCES fornecedores(id_fornecedor),
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id_usuario)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS financeiro (
                    id_financeiro INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL CHECK(tipo IN (
                        \'entrada\', \'saida\'
                    )),
                    valor REAL NOT NULL,
                    descricao TEXT,
                    data TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
        print("BANCO DE DADOS CRIADO!")

if __name__ == '__main__':
    db_manager = DatabaseManager()
    db_manager.create_tables()



