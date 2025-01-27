from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco de dados
DATABASE_URL = "sqlite:///./api_food.db"

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Cria uma sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Cria a classe base para os modelos
Base = declarative_base()

def init_db():
  import app.models  # Importe seus modelos aqui
  # Cria todas as tabelas no banco de dados
  Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()