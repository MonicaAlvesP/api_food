from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# Definindo um OAuth2PasswordBearer para autenticação de token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Chave secreta para JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# Modelo de Usuário (exemplo simples)
class User(BaseModel):
    username: str

# Simulando um banco de usuários
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "adminpassword",  # Em produção, use hash de senha
    }
}

# Função para verificar o token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Função para gerar token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Modelo para alimentos
class Food(BaseModel):
    nome: str
    preco: float
    tipo: str
    imagem: str

foods_db = []

# Rota pública (GET)
@app.get("/foods")
def get_foods():
    return foods_db

# Rota protegida (POST)
@app.post("/foods")
def create_food(food: Food, username: str = Depends(verify_token)):
    if username != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    foods_db.append(food)
    return {"message": "Food added successfully"}

# Rota protegida (PUT/PATCH)
@app.put("/foods/{food_id}")
def update_food(food_id: int, food: Food, username: str = Depends(verify_token)):
    if username != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if 0 <= food_id < len(foods_db):
        foods_db[food_id] = food
        return {"message": "Food updated successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")

# Rota protegida (DELETE)
@app.delete("/foods/{food_id}")
def delete_food(food_id: int, username: str = Depends(verify_token)):
    if username != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if 0 <= food_id < len(foods_db):
        del foods_db[food_id]
        return {"message": "Food deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")

# Rota para gerar o token de autenticação
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordBearer):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
