# Em erp_refatorado/config.py

import os

# Pega o caminho absoluto da pasta onde este arquivo (config.py) está
# que é a raiz do seu projeto.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho completo para o banco de dados, que agora está
# corretamente dentro da pasta 'database'.
DB_PATH = os.path.join(BASE_DIR, 'database', 'clientes.bd')