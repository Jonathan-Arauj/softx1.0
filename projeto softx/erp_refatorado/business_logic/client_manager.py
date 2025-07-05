from erp_refatorado.database.database_manager import DatabaseManager
from erp_refatorado.models.models import Client

class ClientManager:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def add_client(self, client: Client):
        with self.db_manager as cursor:
            cursor.execute(""" INSERT INTO clientes (nome_cliente, cpf_cliente, email_cliente, telefone_cliente,
                                                       data_nascimento, rua, cep, bairro, cidade) 
                                                       VALUES (?,?,?,?,?,?,?,?,?) """,
                            (client.nome_cliente, client.cpf_cliente, client.email_cliente, client.telefone_cliente,
                             client.data_nascimento, client.rua, client.cep, client.bairro, client.cidade))
        return True

    def get_all_clients(self):
        with self.db_manager as cursor:
            cursor.execute(""" SELECT * FROM clientes ORDER BY nome_cliente ASC; """)
            rows = cursor.fetchall()
            return [Client(id_cliente=row[0], nome_cliente=row[1], cpf_cliente=row[2], email_cliente=row[3],
                           telefone_cliente=row[4], data_nascimento=row[5], rua=row[6], cep=row[7],
                           bairro=row[8], cidade=row[9]) for row in rows]

    def delete_client(self, client_id: int):
        with self.db_manager as cursor:
            cursor.execute("""DELETE FROM clientes WHERE id_cliente = ?""", (client_id,))
        return True

    def update_client(self, client: Client):
        with self.db_manager as cursor:
            cursor.execute(""" 
            UPDATE clientes
            SET nome_cliente = ?, cpf_cliente = ?, email_cliente = ?, telefone_cliente = ?, data_nascimento = ?,
             rua = ?, cep = ?, bairro = ?, cidade = ? WHERE id_cliente = ?""",
                              (client.nome_cliente, client.cpf_cliente, client.email_cliente, client.telefone_cliente,
                               client.data_nascimento, client.rua, client.cep, client.bairro, client.cidade, client.id_cliente))
        return True

    def search_client(self, name: str):
        with self.db_manager as cursor:
            # Prevenção de SQL Injection: usar LIKE com parâmetros
            cursor.execute("SELECT * FROM clientes WHERE nome_cliente LIKE ? ORDER BY nome_cliente ASC", (f'%{name}%',))
            rows = cursor.fetchall()
            return [Client(id_cliente=row[0], nome_cliente=row[1], cpf_cliente=row[2], email_cliente=row[3],
                           telefone_cliente=row[4], data_nascimento=row[5], rua=row[6], cep=row[7],
                           bairro=row[8], cidade=row[9]) for row in rows]






