from erp_refatorado.database.database_manager import DatabaseManager
from erp_refatorado.models.models import User
import bcrypt

class UserManager:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def hash_password(self, password):
        # Hash a password for the first time, with a randomly generated salt
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password, hashed_password):
        # Check if the provided password matches the stored hash
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def add_user(self, user: User):
        hashed_pw = self.hash_password(user.senha)
        with self.db_manager as cursor:
            cursor.execute(""" INSERT INTO usuarios (nome_usuario, cpf_usuario, email_usuario, telefone_usuario,
                                                        data_nascimento, rua, cep, bairro, cidade, senha, tipo, permissao) 
                                                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?) """,
                            (user.nome_usuario, user.cpf_usuario, user.email_usuario, user.telefone_usuario,
                             user.data_nascimento, user.rua, user.cep, user.bairro, user.cidade, hashed_pw, user.tipo, user.permissao))
        return True

    def get_all_users(self):
        with self.db_manager as cursor:
            cursor.execute(""" SELECT * FROM usuarios ORDER BY nome_usuario ASC; """)
            rows = cursor.fetchall()
            return [User(id_usuario=row[0], nome_usuario=row[1], cpf_usuario=row[2], email_usuario=row[3],
                         telefone_usuario=row[4], data_nascimento=row[5], rua=row[6], cep=row[7],
                         bairro=row[8], cidade=row[9], senha=row[10], tipo=row[11], permissao=row[12]) for row in rows]

    def delete_user(self, user_id: int):
        with self.db_manager as cursor:
            cursor.execute("""DELETE FROM usuarios WHERE id_usuario = ?""", (user_id,))
        return True

    # No seu arquivo UserManager.py

    def update_user(self, user: User):
        """
        Atualiza os dados de um usuário no banco de dados.
        A senha só é atualizada se um novo valor for fornecido (não estiver em branco).
        """
        # Se o objeto User veio com um texto no campo senha...
        if user.senha:
            # ...então crie um novo hash e prepare uma query para ATUALIZAR a senha.
            hashed_pw = self.hash_password(user.senha)
            query = """ UPDATE usuarios
                        SET nome_usuario = ?, cpf_usuario = ?, email_usuario = ?, telefone_usuario = ?, 
                            data_nascimento = ?, rua = ?, cep = ?, bairro = ?, cidade = ?, 
                            senha = ?, tipo = ?, permissao = ? 
                        WHERE id_usuario = ? """
            params = (user.nome_usuario, user.cpf_usuario, user.email_usuario, user.telefone_usuario,
                      user.data_nascimento, user.rua, user.cep, user.bairro, user.cidade,
                      hashed_pw, user.tipo, user.permissao, user.id_usuario)
        else:
            # ...se a senha veio vazia, prepare uma query que NÃO TOCA na coluna senha.
            query = """ UPDATE usuarios
                        SET nome_usuario = ?, cpf_usuario = ?, email_usuario = ?, telefone_usuario = ?, 
                            data_nascimento = ?, rua = ?, cep = ?, bairro = ?, cidade = ?, 
                            tipo = ?, permissao = ? 
                        WHERE id_usuario = ? """  # Veja que a coluna 'senha' não está aqui!
            params = (user.nome_usuario, user.cpf_usuario, user.email_usuario, user.telefone_usuario,
                      user.data_nascimento, user.rua, user.cep, user.bairro, user.cidade,
                      user.tipo, user.permissao, user.id_usuario)

        # Executa a query correta que foi montada no if/else
        with self.db_manager as cursor:
            cursor.execute(query, params)

        return True
    def search_user(self, name: str):
        with self.db_manager as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE nome_usuario LIKE ? ORDER BY nome_usuario ASC", (f"%{name}%",))
            rows = cursor.fetchall()
            return [User(id_usuario=row[0], nome_usuario=row[1], cpf_usuario=row[2], email_usuario=row[3],
                         telefone_usuario=row[4], data_nascimento=row[5], rua=row[6], cep=row[7],
                         bairro=row[8], cidade=row[9], senha=row[10], tipo=row[11], permissao=row[12]) for row in rows]

    def get_user_by_id(self, user_id: int):
        with self.db_manager as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(id_usuario=row[0], nome_usuario=row[1], cpf_usuario=row[2], email_usuario=row[3],
                            telefone_usuario=row[4], data_nascimento=row[5], rua=row[6], cep=row[7],
                            bairro=row[8], cidade=row[9], senha=row[10], tipo=row[11], permissao=row[12])
            return None

    def authenticate_user(self, username, password):
        """
        Verifica se um usuário e senha são válidos.
        Retorna o objeto User se a autenticação for bem-sucedida, senão None.
        """
        try:
            # Busca o usuário pelo nome de usuário (que deve ser único)
            user_to_check = self.get_user_by_username(username)

            if user_to_check and self.check_password(password, user_to_check.senha):
                return user_to_check
        except Exception as e:
            print(f"Erro durante a autenticação: {e}")

        return None

    def get_user_by_username(self, username):
        """Busca um único usuário pelo nome de usuário."""
        with self.db_manager as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE nome_usuario = ?", (username,))
            row = cursor.fetchone()
            if row:
                # Adapte os índices (row[0], row[1], etc.) para a ordem das colunas da sua tabela
                return User(id_usuario=row[0], nome_usuario=row[1], cpf_usuario=row[2],
                            email_usuario=row[3], telefone_usuario=row[4],
                            data_nascimento=row[5], rua=row[6], cep=row[7],
                            bairro=row[8], cidade=row[9], senha=row[10],
                            tipo=row[11], permissao=row[12])
        return None






