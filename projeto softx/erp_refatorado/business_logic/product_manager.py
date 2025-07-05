from erp_refatorado.database.database_manager import DatabaseManager
from erp_refatorado.models.models import Product, Stock

class ProductManager:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def add_product(self, product: Product, initial_stock: int = 0):
        with self.db_manager as cursor:
            cursor.execute(""" INSERT INTO produtos (nome, descricao, preco_venda, preco_compra, fornecedor_id) 
                                                       VALUES (?,?,?,?,?) """,
                            (product.nome, product.descricao, product.preco_venda, product.preco_compra, product.fornecedor_id))
            product_id = cursor.lastrowid
            if product_id and initial_stock > 0:
                cursor.execute(""" INSERT INTO estoque (produto_id, quantidade) VALUES (?,?) """, (product_id, initial_stock))
        return True

    def get_all_products(self):
        with self.db_manager as cursor:
            cursor.execute(""" SELECT p.*, s.quantidade FROM produtos p LEFT JOIN estoque s ON p.id_produto = s.produto_id ORDER BY p.nome ASC; """)
            rows = cursor.fetchall()
            products = []
            for row in rows:
                product = Product(id_produto=row[0], nome=row[1], descricao=row[2], preco_venda=row[3],
                                  preco_compra=row[4], fornecedor_id=row[5])
                product.stock_quantity = row[6] if row[6] is not None else 0 # Adiciona a quantidade em estoque
                products.append(product)
            return products

    def delete_product(self, product_id: int):
        with self.db_manager as cursor:
            cursor.execute("""DELETE FROM estoque WHERE produto_id = ?""", (product_id,))
            cursor.execute("""DELETE FROM produtos WHERE id_produto = ?""", (product_id,))
        return True

    def update_product(self, product: Product):
        with self.db_manager as cursor:
            cursor.execute(""" 
            UPDATE produtos
            SET nome = ?, descricao = ?, preco_venda = ?, preco_compra = ?, fornecedor_id = ? WHERE id_produto = ?""",
                              (product.nome, product.descricao, product.preco_venda, product.preco_compra, product.fornecedor_id, product.id_produto))
        return True

    def update_stock(self, product_id: int, quantity: int):
        with self.db_manager as cursor:
            cursor.execute(""" INSERT OR REPLACE INTO estoque (produto_id, quantidade) VALUES (?, (SELECT COALESCE(quantidade, 0) FROM estoque WHERE produto_id = ?) + ?) """,
                            (product_id, product_id, quantity))
        return True

    def search_product(self, name: str):
        with self.db_manager as cursor:
            cursor.execute("SELECT * FROM produtos WHERE nome LIKE ? ORDER BY nome ASC", (f"%{name}%",))
            rows = cursor.fetchall()
            products = []
            for row in rows:
                product = Product(id_produto=row[0], nome=row[1], descricao=row[2], preco_venda=row[3],
                                  preco_compra=row[4], fornecedor_id=row[5])
                product.stock_quantity = row[6] if row[6] is not None else 0
                products.append(product)
            return products






