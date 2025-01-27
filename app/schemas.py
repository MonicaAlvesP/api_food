from pydantic import BaseModel

# Modelo base para a classe Food
class FoodBase(BaseModel):
    tipo: str
    nome: str
    imagem: str
    preco: float

# Modelo para criação de um novo Food (não inclui o ID)
class FoodCreate(FoodBase):
    pass

# Modelo para o retorno de um Food, já incluindo o ID
class Food(FoodBase):
    id: int

    class Config:
        orm_mode = True  # Permite que o Pydantic trabalhe com modelos ORM

# Modelo para atualização de um Food (todos os campos são opcionais)
class FoodUpdate(BaseModel):
    tipo: str | None = None
    nome: str | None = None
    imagem: str | None = None
    preco: float | None = None

    class Config:
        orm_mode = True
