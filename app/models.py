from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Instância base para modelos
Base = declarative_base()

# Modelo da tabela "foods"
class Food(Base):
    __tablename__ = "foods"  # Nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True)  # ID único e chave primária
    tipo = Column(String(50), nullable=False)  # Tipo de comida, tamanho máximo 50
    nome = Column(String(100), nullable=False, index=True)  # Nome do item, indexado
    imagem = Column(String(255))  # URL da imagem (tamanho adequado para URLs)
    preco = Column(Float, nullable=False)  # Preço do item
