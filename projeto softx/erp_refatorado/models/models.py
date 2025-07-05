from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id_usuario: Optional[int] = None
    nome_usuario: str = field(default="")
    cpf_usuario: str = field(default="")
    email_usuario: str = field(default="")
    telefone_usuario: str = field(default="")
    data_nascimento: str = field(default="")
    rua: str = field(default="")
    cep: str = field(default="")
    bairro: str = field(default="")
    cidade: str = field(default="")
    senha: str = field(default="")
    tipo: str = field(default="vendedor") # admin, vendedor, financeiro, estoque
    permissao: str = field(default="padrao")

@dataclass
class Client:
    id_cliente: Optional[int] = None
    nome_cliente: str = field(default="")
    cpf_cliente: str = field(default="")
    email_cliente: str = field(default="")
    telefone_cliente: str = field(default="")
    data_nascimento: str = field(default="")
    rua: str = field(default="")
    cep: str = field(default="")
    bairro: str = field(default="")
    cidade: str = field(default="")

@dataclass
class Supplier:
    id_fornecedor: Optional[int] = None
    nome: str = field(default="")
    cnpj: str = field(default="")
    telefone: Optional[str] = None
    email: Optional[str] = None
    rua: str = field(default="")
    cep: str = field(default="")
    bairro: str = field(default="")
    cidade: str = field(default="")

@dataclass
class Product:
    id_produto: Optional[int] = None
    nome: str = field(default="")
    descricao: Optional[str] = None
    preco_venda: float = field(default=0.0)
    preco_compra: float = field(default=0.0)
    fornecedor_id: Optional[int] = None

@dataclass
class Stock:
    id_estoque: Optional[int] = None
    produto_id: int = field(default=0)
    quantidade: int = field(default=0)

@dataclass
class Sale:
    id_vendas: Optional[int] = None
    cliente_id: int = field(default=0)
    usuario_id: int = field(default=0)
    data_venda: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    total: float = field(default=0.0)

@dataclass
class Purchase:
    id_compras: Optional[int] = None
    fornecedor_id: int = field(default=0)
    usuario_id: int = field(default=0)
    data_compra: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    total: float = field(default=0.0)

@dataclass
class Financial:
    id_financeiro: Optional[int] = None
    tipo: str = field(default="entrada") # entrada, saida
    valor: float = field(default=0.0)
    descricao: Optional[str] = None
    data: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


