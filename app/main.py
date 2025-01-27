from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import Base, Food
from app.schemas import FoodCreate, Food as FoodSchema, FoodUpdate

# Configurações do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./food.db"  # O caminho do seu banco SQLite

# Criação do engine e da sessão do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação do FastAPI app
app = FastAPI()

# Função para criar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criação do banco de dados, se não existir
Base.metadata.create_all(bind=engine)

# Endpoints para manipular os alimentos

@app.post("/foods/", response_model=FoodSchema)
def create_food(food: FoodCreate, db: Session = Depends(get_db)):
    db_food = Food(nome=food.nome, tipo=food.tipo, imagem=food.imagem, preco=food.preco)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

@app.get("/foods/{food_id}", response_model=FoodSchema)
def read_food(food_id: int, db: Session = Depends(get_db)):
    db_food = db.query(Food).filter(Food.id == food_id).first()
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return db_food

@app.put("/foods/{food_id}", response_model=FoodSchema)
def update_food(food_id: int, food: FoodUpdate, db: Session = Depends(get_db)):
    db_food = db.query(Food).filter(Food.id == food_id).first()
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")

    for key, value in food.dict(exclude_unset=True).items():
        setattr(db_food, key, value)

    db.commit()
    db.refresh(db_food)
    return db_food

@app.delete("/foods/{food_id}", response_model=FoodSchema)
def delete_food(food_id: int, db: Session = Depends(get_db)):
    db_food = db.query(Food).filter(Food.id == food_id).first()
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")

    db.delete(db_food)
    db.commit()
    return db_food
