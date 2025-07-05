from erp_refatorado.database.database_manager import DatabaseManager
from erp_refatorado.models.models import Supplier

class SupplierManager:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def add_supplier(self, supplier: Supplier):
        with self.db_manager as cursor:
            cursor.execute(""" INSERT INTO fornecedores (nome, cnpj, telefone, email, rua, cep, bairro, cidade) 
                                                       VALUES (?,?,?,?,?,?,?,?) """,
                            (supplier.nome, supplier.cnpj, supplier.telefone, supplier.email, supplier.rua,
                             supplier.cep, supplier.bairro, supplier.cidade))
        return True

    def get_all_suppliers(self):
        with self.db_manager as cursor:
            cursor.execute(""" SELECT * FROM fornecedores ORDER BY nome ASC; """)
            rows = cursor.fetchall()
            return [Supplier(id_fornecedor=row[0], nome=row[1], cnpj=row[2], telefone=row[3], email=row[4],
                             rua=row[5], cep=row[6], bairro=row[7], cidade=row[8]) for row in rows]

    def delete_supplier(self, supplier_id: int):
        with self.db_manager as cursor:
            cursor.execute("""DELETE FROM fornecedores WHERE id_fornecedor = ?""", (supplier_id,))
        return True

    def update_supplier(self, supplier: Supplier):
        with self.db_manager as cursor:
            cursor.execute(""" 
            UPDATE fornecedores
            SET nome = ?, cnpj = ?, telefone = ?, email = ?, rua = ?, cep = ?, bairro = ?, cidade = ? WHERE id_fornecedor = ?""",
                              (supplier.nome, supplier.cnpj, supplier.telefone, supplier.email, supplier.rua,
                               supplier.cep, supplier.bairro, supplier.cidade, supplier.id_fornecedor))
        return True

    def search_supplier(self, name: str):
        with self.db_manager as cursor:
            cursor.execute("SELECT * FROM fornecedores WHERE nome LIKE ? ORDER BY nome ASC", (f"%{name}%",))
            rows = cursor.fetchall()
            return [Supplier(id_fornecedor=row[0], nome=row[1], cnpj=row[2], telefone=row[3], email=row[4],
                             rua=row[5], cep=row[6], bairro=row[7], cidade=row[8]) for row in rows]






